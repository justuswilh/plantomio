import re

# Pfad zur HTML-Datei
file_path = 'supplyu95overview.html'

# Lesen Sie die HTML-Datei ein
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Regulärer Ausdruck zum Finden und Ersetzen
pattern = r'src="img/([^"]+\.svg)"'
replacement = r'src="{% static \'img/\1\' %}"'

# Ersetzen der Vorkommen
new_content = re.sub(pattern, replacement, content)

# Schreiben Sie die Änderungen zurück in die HTML-Datei
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(new_content)

print("Ersetzungen abgeschlossen.")