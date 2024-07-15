import requests
import datetime
import time
import json
import os
import urllib.parse
import logging
import sys
import sqlite3
import subprocess

pumping_required = True
dry_soil_border=int (35)
wet_soil_border=int (40)
flooded_soil_border=int (55)
pumpingCycle=0

def getMoisture(address):
    try:
        querystring="http://" + "localhost" +':9090/api/v1/query?query=flowercare_moisture_percent{macaddress="'+ str(address) + '"}[60s]'
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
                    print(address, ':', sensor_moisture)
                    return(sensor_moisture)
                
                except Exception as e:
                    logging.error("Fehler beim Verarbeiten der Ergebnisse: ", e)
                    print("Fehler beim Verarbeiten der Ergebnisse: ", e)
    except requests.exceptions.RequestException as err:
        logging.error("Fehler bei der Anfrage: ", err)
        print("Fehler bei der Anfrage: ", err)

def runPump(irrigationProgram, pump_address, plant_monitor_addresses, targetMoisture, targetHysteresisTop, group):
    ####### irrigationProgram= 1 normal, 4 langsam #######
  
    plant_monitor_addresses = plant_monitor_addresses.strip('[]').replace("'", "").replace(' ', '')
    address_list = plant_monitor_addresses.split(',')    
    global pumpingCycle
    global pumping_required
    maxPumpingCycle= 0
    irrigationProgram = int(irrigationProgram)
    if (irrigationProgram == 1):
        pumpCycleDelay= 250  
        pump_duration= 100   
        maxPumpingCycle= 7
           

    if irrigationProgram == 4:
        pumpCycleDelay= 250  
        pump_duration= 50     
        maxPumpingCycle= 14

    if (irrigationProgram == 0):
        logging.info("No irrigation program defined")
        print("No irrigation program defined")
        sys.exit()

    while (pumping_required and pumpingCycle < maxPumpingCycle):
        pumpingCycle+=1 
        turn_on="cm?cmnd=Backlog%20Power%20On%3BDelay%20"
        turn_off="%3BPower%20Off%3b"                               
        print("Pumpenzyklus: " + str(pumpingCycle) + ' Gruppe: ' + str(group) + " Bewässerungsprogramm: " + 
        str(irrigationProgram) + " für " + str(pump_duration) + " Sekunden, mit " + str(pumpCycleDelay) + " Sekunden Pause")
        logging.info("Running pump for "+str(pump_duration)+" seconds")
        # Tasmota delay is in units of 0.1 seconds for a value between 2..3600
        if (pump_duration<3600): 
            pump_duration_tasmota=pump_duration*10
        else:
            pump_duration_tasmota=3600*10
            logging.error("Pump duration out of range; truncated to 3600")
        pump_cmd_string=turn_on+str(pump_duration_tasmota)+turn_off
        pumpstring="http://"+(pump_address)+'/'+pump_cmd_string
       
        try:
            r1=requests.get(pumpstring)
            r1.raise_for_status()
        except Exception:
                print("Error occurred while making the request:")

        time.sleep(pumpCycleDelay)


        for address in address_list:
            targetMoisture = int(targetMoisture)
            targetHysteresisTop = int(targetHysteresisTop)
            moisture = getMoisture(address)
            if moisture is None:
                logging.info("Couldn't get sensor data")
                print(address, ':', "Couldn't get sensor data")
            else:
                if moisture < targetMoisture + targetHysteresisTop:
                    pumping_required = True
                    print("Bewässerung weiterhing erforderlich")
                    break
                if moisture > targetMoisture + targetHysteresisTop:
                    pumping_required = False
                    print("Pumping not required")
                    
    if (pumping_required and pumpingCycle >= maxPumpingCycle):
        logging.info("Reached max. pumping cycle but still not enough")
        print("Reached max. pumping cycle but still not enough")
        sys.exit()

    if not pumping_required:
        print("Moisture OK")
        logging.info("Moisture OK")
        sys.exit()
    
runPump(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
