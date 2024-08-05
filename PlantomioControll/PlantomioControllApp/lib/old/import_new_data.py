# filename: import_to_sqlite.py
import csv
import sqlite3
import os

# Pfad CSV-Datei
biodata_path = 'biodata_source.csv'
devicelist_path = 'devicelist_source.csv'

# Pfad SQLite-Datenbankdatei
biodata_sql_path = 'biodata.db'
devicelist_sql_path = 'devicelist.db'


# Stelle sicher, dass die CSV-Datei existiert
if not os.path.exists(biodata_path):
    raise Exception(f"Die CSV-Datei unter {biodata_path} wurde nicht gefunden.")

if not os.path.exists(devicelist_path):
    raise Exception(f"Die CSV-Datei unter {devicelist_path} wurde nicht gefunden.")

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(biodata_sql_path)
cursor = conn.cursor()

# Tabelle cannabis1 löschen
cursor.execute('DROP TABLE IF EXISTS cannabis1')

# Erstelle eine Tabelle in der Datenbank (angepasst an deine Datenstruktur)
# Hinweis: Die Spaltennamen und Datentypen müssen entsprechend deiner CSV-Datei angepasst werden
cursor.execute('''
CREATE TABLE IF NOT EXISTS cannabis1 (
    plan TEXT,
    week INTEGER,
    phase TEXT,
    target_moisture REAL,
    target_moisture_hysteresis_top REAL,
    target_moisture_hysteresis_bot REAL,
    target_brightness REAL,
    light_hours REAL,
    target_ec REAL,
    target_ec_hysteresis REAL,
    target_ph REAL,
    target_ph_hysteresis REAL,
    target_temperature REAL,
    target_temperature_hysteresis REAL,
    target_humidity REAL,
    target_humidity_hysteresis_top REAL,
    target_humidity_hysteresis_bot REAL,
    to_do TEXT
)
''')

char_enc = 'utf-8'

# Öffne die CSV-Datei und lese die Daten
with open(biodata_path, newline='', encoding=char_enc, errors='ignore') as csvfile1:
    csv_reader = csv.DictReader(csvfile1, delimiter=';')
    biodata_to_insert = [(row['plan'], row['week'], row['phase'], row['target_moisture'], row['target_moisture_hysteresis_top'], row['target_moisture_hysteresis_bot'], row['target_brightness'], row['light_hours'], row['target_ec'], row['target_ec_hysteresis'], row['target_ph'], row['target_ph_hysteresis'], row['target_temperature'], row['target_temperature_hysteresis'], row['target_humidity'], row['target_humidity_hysteresis_top'], row['target_humidity_hysteresis_bot'], row['to_do']) for row in csv_reader]

# Füge die Daten in die SQLite-Datenbank ein
cursor.executemany('INSERT INTO cannabis1 (plan, week, phase, target_moisture, target_moisture_hysteresis_top, target_moisture_hysteresis_bot, target_brightness, light_hours, target_ec, target_ec_hysteresis, target_ph, target_ph_hysteresis, target_temperature, target_temperature_hysteresis, target_humidity, target_humidity_hysteresis_top, target_humidity_hysteresis_bot, to_do) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', biodata_to_insert)
# Committe die Änderungen und schließe die Verbindung
conn.commit()
conn.close()

print('Bio-Daten wurden erfolgreich in die SQLite-Datenbank importiert.')

############################################################################################################


# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(devicelist_sql_path)
cursor = conn.cursor()

# Tabelle devices löschen
cursor.execute('DROP TABLE IF EXISTS devices')

# Erstelle eine Tabelle in der Datenbank (angepasst an deine Datenstruktur)
# Hinweis: Die Spaltennamen und Datentypen müssen entsprechend deiner CSV-Datei angepasst werden
cursor.execute('''
CREATE TABLE IF NOT EXISTS devices (
    type TEXT,
    name TEXT,
    adress TEXT,
    username TEXT,
    password TEXT,
    role TEXT,
    "group" TEXT
)
''')

char_enc = 'utf-8'

# Öffne die CSV-Datei und lese die Daten
with open(devicelist_path, newline='', encoding=char_enc, errors='ignore') as csvfile2:
    csv_reader = csv.DictReader(csvfile2, delimiter=';')
    devices_to_insert = [(row['type'], row['name'], row['adress'], row['username'], row['password'], row['role'], row['group']) for row in csv_reader]

# Füge die Daten in die SQLite-Datenbank ein
cursor.executemany('INSERT INTO devices (type, name, adress, username, password, role, "group") VALUES (?, ?, ?, ?, ?, ?, ?)', devices_to_insert)
# Committe die Änderungen und schließe die Verbindung
conn.commit()
conn.close()

print('Die Devicelist wurden erfolgreich in die SQLite-Datenbank importiert.')