def runPump(irrigationProgram,pump_adress,):
    pumping_required = True
    maxPumpingCycle= 7
    pumpCycleDelay= 250  
    pump_duration= 100      
    dry_soil_border=int (35)
    wet_soil_border=int (40)
    flooded_soil_border=int (55)
    targetHysteresisTop= 10  
    global pumpingCycle
    print (pumpingCycle)

def getMoisture(device):
    try:
        querystring="http://" + (configdata['system_config']['prometheus_ip']) +':9090/api/v1/query?query=flowercare_moisture_percent{macaddress="'+ str(device['address']) + '"}[60s]'
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
                    group = device['group']
                    print(sensor_moisture, device['address'])
                    return(sensor_moisture, group)
                
                except Exception as e:
                    logging.error("Fehler beim Verarbeiten der Ergebnisse: ", e)
    except requests.exceptions.RequestException as err:
        logging.error("Fehler bei der Anfrage: ", err)







    run20s="cm?cmnd=Backlog%20Power%20On%3BDelay%20200%3BPower%20Off%3b"
    runpump1="cm?cmnd=Backlog%20Power%20On%3BDelay%20"
    runpump2="%3BPower%20Off%3b"


    if pumping_required & pumpingCycle < maxPumpingCycle:
        pumpingCycle+=1                                
        print("Pumping cycle: "+str(pumpingCycle))
        if irrigationProgram == 1 or 3:
            print("Pumping cycle: "+str(pumpingCycle))
            logging.info("Running pump for "+str(pump_duration)+" seconds")
            # Tasmota delay is in units of 0.1 seconds for a value between 2..3600
            if (pump_duration<3600): 
                pump_duration_tasmota=pump_duration*10
            else:
                pump_duration_tasmota=3600*10
                logging.error("Pump duration out of range; truncated to 3600")
            pump_cmd_string=runpump1+str(pump_duration_tasmota)+runpump2
            print("running pump using Plug "+('192.168.188.151'))
            pumpstring="http://"+('192.168.188.151')+'/'+pump_cmd_string
            r1=requests.get(pumpstring)
            print("wait pumpCycleDelay:"+str(pumpCycleDelay))
            time.sleep(pumpCycleDelay)
            checkMoisture()