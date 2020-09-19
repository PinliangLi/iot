import bluetooth

near = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(near)))
target_name = "iPhone"
for addr, name in near:
    print("{} --> {}".format(addr, name))
    if target_name == name:
    	device = (addr, name)
    	print(device)