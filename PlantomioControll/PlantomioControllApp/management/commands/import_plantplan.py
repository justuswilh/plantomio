import csv
import sqlite3
import os

# Pfad zur CSV-Datei
csv_path = 'PlantomioControll/static/csv/biodata_source.csv'

# Pfad zur SQLite-Datenbankdatei
sqlite_path = 'PlantomioControll/db.sqlite3'

# Stelle sicher, dass die CSV-Datei existiert
if not os.path.exists(csv_path):
    raise Exception(f"Die CSV-Datei unter {csv_path} wurde nicht gefunden.")

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(sqlite_path)
cursor = conn.cursor()

# Tabelle plantplanvalue löschen, falls sie existiert
cursor.execute('DROP TABLE IF EXISTS PlantomioControllApp_plantplanvalue')

# Erstelle eine Tabelle in der Datenbank (angepasst an das PlantPlanValue-Modell)
cursor.execute('''
CREATE TABLE IF NOT EXISTS PlantomioControllApp_plantplanvalue (
    planId TEXT,
    week TEXT,
    phase TEXT,
    moistureTarget TEXT,
    moistureMinimum TEXT,
    moistureMaximum TEXT,
    brightnessTarget TEXT,
    brightnessMinimum TEXT,
    brightnessMaximum TEXT,
    lighthoursTarget TEXT,
    lighthoursMinimum TEXT,
    lighthoursMaximum TEXT,
    ecTarget TEXT,
    ecMinimum TEXT,
    ecMaximum TEXT,
    phTarget TEXT,
    phMinimum TEXT,
    phMaximum TEXT,
    temperatureTarget TEXT,
    temperatureMinimum TEXT,
    temperatureMaximum TEXT,
    humidityTarget TEXT,
    humidityMinimum TEXT,
    humidityMaximum TEXT,
    information TEXT
)
''')

char_enc = 'utf-8'

# Öffne die CSV-Datei und lese die Daten
try:
    with open(csv_path, newline='', encoding=char_enc, errors='ignore') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        
        # Überprüfe die Spaltennamen
        csv_headers = csv_reader.fieldnames
        expected_headers = [
            'planId', 'week', 'phase', 'moistureTarget', 'moistureMinimum', 'moistureMaximum',
            'brightnessTarget', 'brightnessMinimum', 'brightnessMaximum', 'lighthoursTarget', 'lighthoursMinimum',
            'lighthoursMaximum', 'ecTarget', 'ecMinimum', 'ecMaximum', 'phTarget', 'phMinimum',
            'phMaximum', 'temperatureTarget', 'temperatureMinimum', 'temperatureMaximum', 'humidityTarget',
            'humidityMinimum', 'humidityMaximum', 'information'
        ]
        
        if csv_headers != expected_headers:
            raise ValueError(f"Die CSV-Datei enthält nicht die erwarteten Spalten. Erwartet: {expected_headers}, Gefunden: {csv_headers}")
        
        plant_plan_values_to_insert = [
            (
                row['planId'], row['week'], row['phase'], row['moistureTarget'], row['moistureMinimum'], row['moistureMaximum'],
                row['brightnessTarget'], row['brightnessMinimum'], row['brightnessMaximum'], row['lighthoursTarget'], row['lighthoursMinimum'],
                row['lighthoursMaximum'], row['ecTarget'], row['ecMinimum'], row['ecMaximum'], row['phTarget'], row['phMinimum'],
                row['phMaximum'], row['temperatureTarget'], row['temperatureMinimum'], row['temperatureMaximum'], row['humidityTarget'],
                row['humidityMinimum'], row['humidityMaximum'], row['information']
            ) for row in csv_reader
        ]
except Exception as e:
    print(f"Fehler beim Lesen der CSV-Datei: {e}")
    conn.close()
    raise

# Füge die Daten in die SQLite-Datenbank ein
try:
    cursor.executemany('''
    INSERT INTO PlantomioControllApp_plantplanvalue (
        planId, week, phase, moistureTarget, moistureMinimum, moistureMaximum, brightnessTarget, brightnessMinimum, brightnessMaximum,
        lighthoursTarget, lighthoursMinimum, lighthoursMaximum, ecTarget, ecMinimum, ecMaximum, phTarget, phMinimum, phMaximum,
        temperatureTarget, temperatureMinimum, temperatureMaximum, humidityTarget, humidityMinimum, humidityMaximum, information
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', plant_plan_values_to_insert)
    
    # Committe die Änderungen und schließe die Verbindung
    conn.commit()
    print('PlantPlanValue-Daten wurden erfolgreich in die SQLite-Datenbank importiert.')
except sqlite3.Error as e:
    print(f"Fehler beim Einfügen der Daten in die SQLite-Datenbank: {e}")
finally:
    conn.close()

