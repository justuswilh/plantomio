##structure control.py
# 0. check configuration changes
# 1. load system configurations
# 2. load devices
# 3. organise devices
# 4. config supply


import requests
import datetime
import json
import urllib.parse
import logging
import sys
import sqlite3
import subprocess
import multiprocessing
import csv
import moistureController

olimexIP= 'plantomio-dev.ddns.net'
configFile='config.json'
configLog='plantomio_start.log'
configfile_modification_time=0
pumpingCycle=0 

logging.basicConfig(filename=configLog, encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s  :')
logging.info('******** Plantomio_control started')
    
# 0. check configuration changes
# def checkChanges():
#     try: 
#         modification_time = os.path.getmtime(configFile)        
#         local_time = time.ctime(modification_time)
#         logging.info("config file last modification time (local time):", time.ctime(modification_time))
#     except OSError:
#         logging.error("Path '%s' for the config file does not exists or is inaccessible")
#         sys.exit()
#     if (modification_time!=configfile_modification_time):
#         configfile_modification_time=modification_time
#         return True
#     else:
#         return False
    
# 1. load system configurations    
def loadConfig():    
    try:
        with open(configFile) as f:
            return json.load(f)
       
    except OSError:
        logging.error("Config file '%s' could not be loaded" %configFile)
        sys.exit()

configData=loadConfig()


# Funktion, um das jüngste "start_grow"-Datum aus der CSV-Datei zu ermitteln
def get_latest_start_grow_date(csv_file):
    latest_date = None    
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            headers = reader.fieldnames  # List of field names
            #print(f"CSV-Spalten: {headers}")  # Debugging-Ausgabe der Spaltennamen
            for row in reader:
                #print(f"Zeile: {row}")  # Debugging-Ausgabe jeder Zeile
                if 'Typ' in row and row['Typ'] == 'start_grow':
                    entry_date = datetime.datetime.strptime(row['Datum'], '%d.%m.%Y').date()
                    if latest_date is None or entry_date > latest_date:
                        latest_date = entry_date
        return latest_date
    except: logging.error("Config file '%s' could not be loaded" %configFile)

# Jüngstes "start_grow"-Datum aus der plantlog_source.csv-Datei ermitteln
start_date = get_latest_start_grow_date('plantlog_source.csv')
today = datetime.date.today()
delta = today - start_date
current_week = delta.days // 7
current_week_day = delta.days % 7
plant_plan_table = 'cannabis1'

def loadBiadata():
    global current_week
    global plant_plan_table
    try:
        conn = sqlite3.connect('biodata.db')
        cursor = conn.cursor()

        # Daten abrufen
        cursor.execute(f'SELECT * FROM {plant_plan_table} LIMIT 1')
        column_names = [description[0] for description in cursor.description]


        # Finden Sie die Position der relevanten Spalten
        phase_index = column_names.index('phase')
        target_moisture_index = column_names.index('target_moisture')
        target_moisture_hysteresis_top_index = column_names.index('target_moisture_hysteresis_top')
        target_moisture_hysteresis_bot_index = column_names.index('target_moisture_hysteresis_bot')
        target_brightness_index = column_names.index('target_brightness')
        light_hours_index = column_names.index('light_hours')
        target_ec_index = column_names.index('target_ec')
        target_ec_hysteresis_index = column_names.index('target_ec_hysteresis')
        target_ph_index = column_names.index('target_ph')
        target_ph_hysteresis_index = column_names.index('target_ph_hysteresis')
        target_temperature_index = column_names.index('target_temperature')
        target_temperature_hysteresis_index = column_names.index('target_temperature_hysteresis')
        target_humidity_index = column_names.index('target_humidity')
        target_humidity_hysteresis_top_index = column_names.index('target_humidity_hysteresis_top')
        target_humidity_hysteresis_bot_index = column_names.index('target_humidity_hysteresis_bot')
        to_do_index = column_names.index('to_do')

        # Daten abrufen
        cursor.execute(f'SELECT * FROM {plant_plan_table} WHERE week = ?', (current_week,))
        row = cursor.fetchone()
        print(row)
        phase = row[phase_index]
        target_moisture = int(row[target_moisture_index])
        target_moisture_hysteresis_top = int(row[target_moisture_hysteresis_top_index])
        target_moisture_hysteresis_bot = int(row[target_moisture_hysteresis_bot_index])
        target_brightness = int(row[target_brightness_index])
        light_hours = int(row[light_hours_index])
        target_ec = int(row[target_ec_index])
        target_ec_hysteresis = int(row[target_ec_hysteresis_index])
        target_ph = int(row[target_ph_index])
        target_ph_hysteresis = int(row[target_ph_hysteresis_index])
        target_temperature = int(row[target_temperature_index])
        target_temperature_hysteresis = int(row[target_temperature_hysteresis_index])
        target_humidity = int(row[target_humidity_index])
        target_humidity_hysteresis_top = int(row[target_humidity_hysteresis_top_index])
        target_humidity_hysteresis_bot = int(row[target_humidity_hysteresis_bot_index])
        to_do = row[to_do_index]
        return phase, target_moisture, target_moisture_hysteresis_top, target_moisture_hysteresis_bot, target_brightness, light_hours, target_ec, target_ec_hysteresis, target_ph, target_ph_hysteresis, target_temperature, target_temperature_hysteresis, target_humidity, target_humidity_hysteresis_top, target_humidity_hysteresis_bot, to_do

    except: logging.error("Config file '%s' could not be loaded" %configFile)

#phase, target_moisture, target_moisture_hysteresis_top, target_moisture_hysteresis_bot, target_brightness, light_hours, target_ec, target_ec_hysteresis, target_ph, target_ph_hysteresis, target_temperature, target_temperature_hysteresis, target_humidity, target_humidity_hysteresis_top, target_humidity_hysteresis_bot, to_do = loadBiadata()

# 2. load devices - ist die Device Datenbank wirklich notwendig? Eine CSV ist kleiner und für den Olimex lokal dementsprechend sinnvoller + kürzt den Code massiv
def loadDevices():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('devicelist.db')
    cursor = conn.cursor()

    # Daten abrufen
    cursor.execute(f'SELECT * FROM devices LIMIT 1')
    column_names = [description[0] for description in cursor.description]

    # Finden Sie die Position der relevanten Spalten
    name_index = column_names.index('name')
    adress_index = column_names.index('adress')
    role_index = column_names.index('role')
    group_index = column_names.index('group')

    plant_monitors = {}
    pump_plugs = {}
    light_plugs = {}

    # devices abrufen      
    cursor.execute(f'SELECT * FROM devices')  
    rows = cursor.fetchall() 
    for row in rows:
        if row[role_index] == 'plant_monitor':
            device_count = len(plant_monitors) + 1
            plant_monitors[f'plant_monitor_{device_count}'] = {
                'device_id': 'plantmonitor_' + str(device_count) + '_g' + row[group_index] ,
                'name': row[name_index],
                'address': row[adress_index],
                'group': row[group_index]
            }

        if row[role_index] == 'pump_plug':
            device_count = len(pump_plugs) + 1
            pump_plugs[f'pump_plug_{device_count}'] = {
                'device_id': 'pump_plug_' + str(device_count) + '_g' + row[group_index] ,
                'name': row[name_index],
                'address': row[adress_index],
                'group': row[group_index]
            }
    
        if row[role_index] == 'light_plug':
            device_count = len(light_plugs) + 1
            light_plugs[f'light_plug_{device_count}'] = {
                'device_id': 'light_plug_' + str(device_count) + '_g' + row[group_index] ,
                'name': row[name_index],
                'address': row[adress_index],
                'group': row[group_index]   
            }
    print(plant_monitors)            
    return plant_monitors, pump_plugs, light_plugs
    

# 3. organise devices
def groupDevices(devices):
    device_group = {}
    for info_type, device_info in devices.items():
        device_group_value = device_info['group']
        if device_group_value not in device_group:
            device_group[device_group_value] = []
        device_group[device_group_value].append(device_info)
#    print(device_group)
    return device_group

def organiseDevices():
    plant_monitors, pump_plugs, light_plugs = loadDevices()
    plant_monitor_group = groupDevices(plant_monitors)
    pump_plug_group = groupDevices(pump_plugs)
    light_plug_group = groupDevices(light_plugs)
    return plant_monitor_group, pump_plug_group, light_plug_group

plant_monitor_group, pump_plug_group, light_plug_group = organiseDevices()

######## 4. config supply##########
# 4.1. config light supply
def configLight_supply():
    for group in light_plug_group.values():
        for device in group:
            light_on_json={
                "Enable":1,
                "Mode":0,
                "Time":configData['plant_config'][0]['light_on_time'],
                "Window":1,
                "Days":"SMTWTFS",
                "Repeat":1,
                "Output":1,
                "Action":1
            }
            light_off_json={
                "Enable":1,
                "Mode":0,
                "Time":configData['plant_config'][0]['light_off_time'], 
                "Window":1,
                "Days":"SMTWTFS",
                "Repeat":1,
                "Output":1,
                "Action":0
            }
            lightcmd="http://" + device['address'] + '/cm?cmnd=Timers%201'
            print(lightcmd)
        
        try:
            r=requests.get(lightcmd)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            logging.error ("OOps: Something Else",err)

        payload=str(urllib.parse.urlencode({'data':json.dumps(light_on_json)}))
        lightcmd="http://" + device['address'] +'/cm?cmnd=Timer1%20'+payload[5:]
        payload=str(urllib.parse.urlencode({'data':json.dumps(light_off_json)}))
        lightcmd1="http://" + device['address'] +'/cm?cmnd=Timer2%20'+payload[5:]        
        r1=requests.get(lightcmd)
        r2=requests.get(lightcmd1,params=json.dumps(light_off_json))

configLight_supply()

#for groupID in Groups:
#   moistureController.startMoistureControl(""" moistureSensorIPs[], pumpIPs[], groupID """)
#   lightController.startLightControl(""" lightIPs[], groupID """) LightController starten
# if __name__ == '__main__':
#             moistureProc = multiprocessing.Process(target=moistureController.startMoistureControl, args=())
#             lightProc = multiprocessing.Process(target=lightController.startLightControl, args=())
#             moistureProc.daemon = True
#             lightProc.daemon = True
#             moistureProc.start()
#             lightProc.start()


def getMoisture(address):
    try:
        querystring="http://" + olimexIP +':9090/api/v1/query?query=flowercare_moisture_percent{macaddress="'+ str(address) + '"}[60s]'
        #print(querystring)

        r = requests.get(querystring)
        #print(r.text)

        if ((r.status_code>=200) & (r.status_code<230)):           
            logging.info(r.text)
            try:
                results=r.json()['data']['result']
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                logging.error("Error decoding JSON response from database")    
                results=''   
            if (len(results)>0):
                try:
                    vals=r.json()['data']['result'][0]['values']
                    logging.info(datetime.datetime.fromtimestamp(int(vals[0][0])).strftime('%Y-%m-%d %H:%M:%S'))
                    sensor_moisture=int(vals[0][1])
                    #print(sensor_moisture)
                    return(sensor_moisture)
                
                except Exception as e:
                    logging.error("Fehler beim Verarbeiten der Ergebnisse: ", e)
                    print("Fehler beim Verarbeiten der Ergebnisse: ", e)
    except requests.exceptions.RequestException as err:
        logging.error("Fehler bei der Anfrage: ", err)
        print("Fehler bei der Anfrage: ", err)


#4.2. config pump supply
def checkMoisture():
    group_moistures={}
    group_moisture_gaps=[]
    sensorCount=0
    moistureDefizit=0
    targetMoisture=45
    targetHysteresisBot= -5   
    targetHysteresisTop= +10
    dry_soil_border= int (35)
    irrigationProgram= 0 # 1-4 slow to fast irrigation
    plant_monitor_addresses = []

    # get values
    for group in plant_monitor_group.values():
        pump_address = 'not found'

        for device in group:
            group = device['group']
            address = device['address']
            plant_monitor_addresses.append(address)
            device_id = device['device_id']

            if group in pump_plug_group:
                pump_address = pump_plug_group[group][0]['address']
            else:
                print(f"Group {group} not found in pump_plug_group")            
            
            sensor_moisture = getMoisture(address)
            print(device_id, ': ', sensor_moisture)
            sensorCount+=1
            if (sensor_moisture is None):
                logging.error("Couldn't get sensor data")
            else:
                logging.info("Moisture:"+str(sensor_moisture))
#                print("Moisture:"+str(sensor_moisture))
                group_moistures[device_id] = sensor_moisture
                group_moisture_gaps.append(sensor_moisture-targetMoisture)

        # check values
        if sensorCount == 0:
            print("No sensor data available")
            logging.error("No sensor data available")
            sys.exit()
        
        if sensorCount > 0:
            #print (group_moistures)
            for device, value in group_moistures.items():
                #print(device, value)
                if (value<(dry_soil_border)):
                    irrigationProgram=4
                if (value<(targetMoisture + targetHysteresisBot)):    
                    moistureDefizit+=1
            if (moistureDefizit >= sensorCount/2) and irrigationProgram < 1:
                    irrigationProgram=1

        if irrigationProgram == 0:
            print("Keine Bewässerung erforderlich")
            logging.info("No irrigation required")
            sys.exit()

        if irrigationProgram > 0:
            subprocess.Popen(["python3", "run_pump.py", str(irrigationProgram), str(pump_address), str(plant_monitor_addresses), str(targetMoisture), str(targetHysteresisTop), str(group)])

        

checkMoisture()