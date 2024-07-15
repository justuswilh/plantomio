import subprocess

def run_program(program):
    process = subprocess.Popen(program, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

#    print(stdout.decode())
#    print(stderr.decode())

# Beispielaufruf
run_program(["ls", "-l"])