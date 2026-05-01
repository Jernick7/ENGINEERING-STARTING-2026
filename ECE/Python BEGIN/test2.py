name = "V Jernick Samuel"
print(f"System Online for {name}")

# This is like reading a sensor input
status = input("Enter radar status (ON/OFF): ")

if status.upper() == "ON":
    print("Radar is spinning... scanning for signals.")
if status.upper()== "OFF" :
    print("Radar is in standby mode.")