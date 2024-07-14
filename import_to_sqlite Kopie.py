# filename: import_to_sqlite.py
import csv
import sqlite3
import os

# Ersetze dies mit dem Pfad zu deiner CSV-Datei
csv_file_path = 'biodata_source.csv'
# Ersetze dies mit dem Pfad zu deiner SQLite-Datenbankdatei
sqlite_db_path = 'biodata.db'

# Stelle sicher, dass die CSV-Datei existiert
if not os.path.exists(csv_file_path):
    raise Exception(f"Die CSV-Datei unter {csv_file_path} wurde nicht gefunden.")

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(sqlite_db_path)
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
    target_brightnes REAL,
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
with open(csv_file_path, newline='', encoding=char_enc, errors='ignore') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=';')
    biodata_to_insert = [(row['plan'], row['week'], row['phase'], row['target_moisture'], row['target_moisture_hysteresis_top'], row['target_moisture_hysteresis_bot'], row['target_brightnes'], row['light_hours'], row['target_ec'], row['target_ec_hysteresis'], row['target_ph'], row['target_ph_hysteresis'], row['target_temperature'], row['target_temperature_hysteresis'], row['target_humidity'], row['target_humidity_hysteresis_top'], row['target_humidity_hysteresis_bot'], row['to_do']) for row in csv_reader]

# Füge die Daten in die SQLite-Datenbank ein
cursor.executemany('INSERT INTO cannabis1 (plan, week, phase, target_moisture, target_moisture_hysteresis_top, target_moisture_hysteresis_bot, target_brightnes, light_hours, target_ec, target_ec_hysteresis, target_ph, target_ph_hysteresis, target_temperature, target_temperature_hysteresis, target_humidity, target_humidity_hysteresis_top, target_humidity_hysteresis_bot, to_do) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', biodata_to_insert)
# Committe die Änderungen und schließe die Verbindung
conn.commit()
conn.close()

print('Daten wurden erfolgreich in die SQLite-Datenbank importiert.')
