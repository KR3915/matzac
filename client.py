import network
import time
sta = network.WLAN(network.STA_IF) #station
sta.active(True)

#pripojit k ESP
sta.connect("ESP-AP", "protabulesa")

for _ in range(20):
    if sta.isconnected():
        break
    print("čekání na připojení...")
    time.sleep(0.5)
if sta.isconnected:
    print(f"pripojeno | IP:  {sta.ifconfig()[0]}")
else:
    print("nefunguje :(((((")


