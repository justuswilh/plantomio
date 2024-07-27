import sys

def main(irrigationProgram, pump_adress, plant_monitor_group):
    print("Running pump with the following arguments:")
    print("irrigationProgram: " + irrigationProgram)
    print("pump_adress: " + pump_adress)
    print("plant_monitor_group: " + plant_monitor_group)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: run_pump.py <irrigationProgram> <pump_adress> <plant_monitor_group>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

