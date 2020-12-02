#!/home/pi/CINS548/MyView/bin/python

import bluetooth
print("\n Scanning for bluetooth devices:")

devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
number_of_devices = len(devices)

print(number_of_devices, " devices found")
for addr, name, device_class in devices:
    print("\n Device: ")
    print("Device Name: %s" % (name))
    print("Device MAC Address: %s" %(addr))
    print("\n")
    print("Device Class: %s" % (device_class))
    print("\n")
