#!/usr/bin/env python
# from prometheus_client.parser import text_string_to_metric_families
import requests
import datetime
import time
import json
import os
import urllib.parse
import logging
import sys

 
config_filename='config.json'
config_logfile='plantomio_start.log'
configfile_modification_time=0

# TODO:
#   - Disable all timers on the pump IPs (for security)
#   - check if WLAN plugs are available; disable light/pump if not available
#   - use history: if one sensor value doesn't change, disable it
#   - add pump duration
# DONE:
#   - add time/date to logging messages
logging.basicConfig(filename=config_logfile, encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s  :')
logging.info('******** Plantomio_control started')

def checkConfig():
    try: 
        modification_time = os.path.getmtime(config_filename)        
        local_time = time.ctime(modification_time)
        logging.info("config file last modification time (local time):", time.ctime(modification_time))
    except OSError:
        logging.error("Path '%s' for the config file does not exists or is inaccessible")
        sys.exit()
    if (modification_time!=configfile_modification_time):
        configfile_modification_time=modification_time
        return True
    else:
        return False
    
def loadConfig():    
        try:
            f=open(config_filename)
            try:
                configdata=json.load(f)
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                logging.error("Error decoding JSON in the config file")    
                sys.exit()        
            f.close()
        except OSError:
            logging.error("Config file '%s' could not be loaded" %config_filename)
            sys.exit()
        return configdata
    
def progTimer(configdata):
    for i in configdata['plant_config']:        
        print("*** "+i['name'])       
        light_on_json={
            "Enable":1,
            "Mode":0,
            "Time":i['light_on_time'], 
            "Window":1,
            "Days":"SMTWTFS",
            "Repeat":1,
            "Output":1,
            "Action":1
         }
        light_off_json={
            "Enable":1,
            "Mode":0,
            "Time":i['light_off_time'], 
            "Window":1,
            "Days":"SMTWTFS",
            "Repeat":1,
            "Output":1,
            "Action":0
        }
        lightcmd="http://"+str(i['lightplug_ip'])+'/cm?cmnd=Timers%201'
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

        # print(r0.text)
        payload=str(urllib.parse.urlencode({'data':json.dumps(light_on_json)}))
        lightcmd="http://"+str(i['lightplug_ip'])+'/cm?cmnd=Timer1%20'+payload[5:]
        payload=str(urllib.parse.urlencode({'data':json.dumps(light_off_json)}))
        lightcmd1="http://"+str(i['lightplug_ip'])+'/cm?cmnd=Timer2%20'+payload[5:]        
        r1=requests.get(lightcmd)
        # print(r1.text)
        r2=requests.get(lightcmd1,params=json.dumps(light_off_json))
        # print(r2.url)
        # print(r2.text)
        
def getMoisture(sensor):
    querystring="http://"+str(configdata['system_config']['prometheus_ip'])+':9090/api/v1/query?query=flowercare_moisture_percent{macaddress="'+str(sensor)+'"}[60s]'

    print(querystring)

    try:
        r = requests.get(querystring)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        logging.error ("OOps: Something Else",err)
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
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                logging.error("Error decoding JSON response data result values")    
                sys.exit()   
            logging.info(datetime.datetime.fromtimestamp(int(vals[0][0])).strftime('%Y-%m-%d %H:%M:%S'))
            sensor1_moisture=int(vals[0][1])
            return(sensor1_moisture)
    else:
        return 0

run20s="cm?cmnd=Backlog%20Power%20On%3BDelay%20200%3BPower%20Off%3b"
runpump1="cm?cmnd=Backlog%20Power%20On%3BDelay%20"
runpump2="%3BPower%20Off%3b"

# pumpstring="http://"+plug1+'/'+run20s
# querystring="http://"+ip_prometheus+':9090/api/v1/query?query=flowercare_moisture_percent{macaddress="'+macaddress1+'"}[10s]'
# program timers for light plugs
configdata=loadConfig()
progTimer(configdata)    


# loop through plants and check their status
# query sensor data for each plant
for i in configdata['plant_config']:        
    pumpingCycle=0
    pumping_required=False
    firstLoop=True
    while (pumping_required|firstLoop):
        firstLoop=False    
        maxPumpingCycle= int(i['pump_max_repetitions'])       
        targetMoisture=int(i['target_moisture'])
        targetHysteresisBot=int(i['target_moisture_hysteresis_bot'])            
        targetHysteresisTop=int(i['target_moisture_hysteresis_top'])            
        pumpCycleDelay=int(i['pump_delay_time'])   
        pump_duration=int(i['pump_duration'])         
        # loop through sensors (one plant can have multiple)
        sensor_moisture=[]
        sensorCountBelow=0
        sensorCountAbove=0
        sensorCount=0
        for sensor in i['flowercare_macaddress']:
            mysensor=getMoisture(sensor)
            if  (mysensor is None):
                logging.error("Couldn't get sensor data")
            else:
                # sensor_moisture.add(mysensor)           
                logging.info("Moisture:"+str(mysensor))
                print(str(sensor)+"     "+str(mysensor))
                sensorCount+=1
                if (mysensor<(targetMoisture-targetHysteresisBot)):
                    sensorCountBelow+=1
                if (mysensor>(targetMoisture+targetHysteresisTop)):    
                    sensorCountAbove+=1                            
        # check if all sensors are below threshold; start pumping cycles            
        if ((sensorCount>0) & (sensorCountBelow==sensorCount)):
            pumping_required=True
            
        if ((sensorCount>0) & (sensorCountAbove==sensorCount)):
            pumping_required=False
            
        if (pumpingCycle>maxPumpingCycle):
            logging.error("Reached max. pumping cycle but still not enough")
            pumping_required=False    
            
        if (pumping_required):    
            pumpingCycle+=1                                
            print("Pumping cycle: "+str(pumpingCycle))
            logging.info("Running pump for "+str(pump_duration)+" seconds")
            # Tasmota delay is in units of 0.1 seconds for a value between 2..3600
            if (pump_duration<3600): 
                pump_duration_tasmota=pump_duration*10
            else:
                pump_duration_tasmota=3600*10
                logging.error("Pump duration out of range; truncated to 3600")
            pump_cmd_string=runpump1+str(pump_duration_tasmota)+runpump2
            print("running pump using Plug "+str(i['pumpplug_ip']))
            pumpstring="http://"+i['pumpplug_ip']+'/'+pump_cmd_string
            r1=requests.get(pumpstring)
            print("wait pumpCycleDelay:"+str(pumpCycleDelay))
            time.sleep(pumpCycleDelay)
        else:
            print("moisture OK")    
print("end")



