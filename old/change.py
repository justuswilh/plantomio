import sqlite3
import json
import datetime
import csv

# JSON-Datei lesen
with open('config.json', 'r') as f:
    data = json.load(f)

# Funktion, um das jüngste "start_grow"-Datum aus der CSV-Datei zu ermitteln
def get_latest_start_grow_date(csv_file):
    latest_date = None
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

# Jüngstes "start_grow"-Datum aus der plantlog_source.csv-Datei ermitteln
start_date = get_latest_start_grow_date('plantlog_source.csv')

# Überprüfen, ob das Datum gefunden wurde
if start_date is None:
    raise ValueError("Kein 'start_grow'-Eintrag in der CSV-Datei gefunden.")

# Heutiges Datum abrufen
today = datetime.date.today()
# Heutige Woche herausfinden
delta = today - start_date
current_week = delta.days // 7
current_week_day = delta.days % 7
plant_plan_table = data['plant_config'][0]['current_plan']

# Verbindung zur SQLite-Datenbank herstellen
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

# Werte in der JSON-Datei aktualisieren
data['plant_config'][0]['start_date'] = str(start_date)
data['plant_config'][0]['current_week'] = int(current_week)
data['plant_config'][0]['current_week_day'] = str(current_week_day)
data['plant_config'][0]['current_phase'] = str(row[phase_index])
data['plant_config'][0]['target_moisture'] = int(row[target_moisture_index])
data['plant_config'][0]['target_moisture_hysteresis_top'] = int(row[target_moisture_hysteresis_top_index])
data['plant_config'][0]['target_moisture_hysteresis_bot'] = int(row[target_moisture_hysteresis_bot_index])
data['plant_config'][0]['target_brightness'] = int(row[target_brightness_index])
data['plant_config'][0]['light_hours'] = int(row[light_hours_index])

# Verbindung zur SQLite-Datenbank schließen
conn.close()

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('devicelist.db')
cursor = conn.cursor()

# Daten abrufen
cursor.execute(f'SELECT * FROM devices LIMIT 1')
column_names = [description[0] for description in cursor.description]

# Finden Sie die Position der relevanten Spalten
type_index = column_names.index('type')
name_index = column_names.index('name')
adress_index = column_names.index('adress')
username_index = column_names.index('username')
password_index = column_names.index('password')
role_index = column_names.index('role')
group_index = column_names.index('group')

# control_device abrufen
cursor.execute(f'SELECT * FROM devices WHERE type = "control_device"')
row = cursor.fetchone()

# Werte in der JSON-Datei aktualisieren
data['system_config']['control_device'] = str(row[name_index])
data['system_config']['control_device_adress'] = str(row[adress_index])

# messurement_devices abrufen
cursor.execute(f'SELECT * FROM devices WHERE type = "messurement_device"')
row = cursor.fetchall()

# Werte in der JSON-Datei aktualisieren
for i, device in enumerate(row):
    data['system_config'][f'messurement_device.{i+1}'] = str(device[name_index])
    data['system_config'][f'messurement_device.{i+1}_adress'] = str(device[adress_index])
    data['system_config'][f'messurement_device.{i+1}_role'] = str(device[role_index])
    data['system_config'][f'messurement_device.{i+1}_group'] = str(device[group_index])

# actuator_device abrufen
cursor.execute(f'SELECT * FROM devices WHERE type = "actuator_device"')
row = cursor.fetchall()

# Werte in der JSON-Datei aktualisieren
for i, device in enumerate(row):
    data['system_config'][f'actuator_device.{i+1}'] = str(device[name_index])
    data['system_config'][f'actuator_device.{i+1}_adress'] = str(device[adress_index])
    data['system_config'][f'actuator_device.{i+1}_role'] = str(device[role_index])
    data['system_config'][f'actuator_device.{i+1}_group'] = str(device[group_index])

# JSON-Datei schreiben
with open('config.json', 'w') as f:
    json.dump(data, f, indent=4)

##################################Überbrückung############################################

# Laden Sie die Daten aus der 'config.json' Datei
with open('config.json', 'r') as f:
    data = json.load(f)

# Initialisieren Sie device_address und device_key
device_address = None
device_key = None

# Gerät mit dem Namen 'flowercare_1' finden
for i in range(1, 100):  # Ersetzen Sie 10 durch die tatsächliche Anzahl von Messgeräten
    key = f'messurement_device.{i}'
    value = data['system_config'].get(key)
    if value == 'flowercare_1':
        device_key = key  # Speichern Sie den Schlüssel des Geräts
        break

# Überprüfen, ob das Gerät gefunden wurde
if device_key is not None:
    # Holen Sie sich die Adresse des Geräts
    device_address = data['system_config'].get(f'{device_key}_adress')
    data['plant_config'][0]['flowercare_macaddress'] = device_address
else:
    print("Gerät 'flowercare_1' nicht gefunden.")

# Initialisieren Sie device_address und device_key
device_address = None
device_key = None

# Gerät mit dem Namen 'pump_plug_1' finden
for i in range(1, 100):  # Ersetzen Sie 10 durch die tatsächliche Anzahl von Messgeräten
    key = f'actuator_device.{i}'
    value = data['system_config'].get(key)
    if value == 'pump_plug_1':
        device_key = key  # Speichern Sie den Schlüssel des Geräts
        break

# Überprüfen, ob das Gerät gefunden wurde
if device_key is not None:
    # Holen Sie sich die Adresse des Geräts
    device_address = data['system_config'].get(f'{device_key}_adress')
    data['plant_config'][0]['pumpplug_ip'] = device_address
else:
    print("Gerät 'pump_plug_1' nicht gefunden.")

# Initialisieren Sie device_address und device_key
device_address = None
device_key = None

# Gerät mit dem Namen 'lightplug_1' finden
for i in range(1, 100):  # Ersetzen Sie 10 durch die tatsächliche Anzahl von Messgeräten
    key = f'actuator_device.{i}'
    value = data['system_config'].get(key)
    if value == 'lightplug_1':
        device_key = key  # Speichern Sie den Schlüssel des Geräts
        break

# Überprüfen, ob das Gerät gefunden wurde
if device_key is not None:
    # Holen Sie sich die Adresse des Geräts
    device_address = data['system_config'].get(f'{device_key}_adress')
    data['plant_config'][0]['lightplug_ip'] = device_address
else:
    print("Gerät 'lightplug_1' nicht gefunden.")


# JSON-Datei schreiben
with open('config.json', 'w') as f:
    json.dump(data, f, indent=4)

# Verbindung schließen
conn.close()
