from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

# Verzeichnis, in dem sich die CSV-Dateien befinden
CSV_DIR = '.'

@app.route('/load-csv', methods=['GET'])
def load_csv():
    file_name = request.args.get('file')
    file_path = os.path.join(CSV_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            csv_content = file.read()
        return jsonify({"csv": csv_content})
    else:
        return jsonify({"error": "Datei nicht gefunden"}), 404

@app.route('/save-csv', methods=['POST'])
def save_csv():
    data = request.json
    csv_content = data.get('csv')
    file_name = data.get('file')
    if csv_content and file_name:
        file_path = os.path.join(CSV_DIR, file_name)
        with open(file_path, 'w') as file:
            file.write(csv_content)
        run_import_script()
        return jsonify({"message": "CSV-Datei erfolgreich gespeichert."}), 200
    else:
        return jsonify({"message": "Keine CSV-Daten erhalten."}), 400

def run_import_script():
    try:
        result = subprocess.run(['python', 'import_new_data.py'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"Fehler beim Ausführen des Skripts: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
