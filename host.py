from logic import *
import network
import socket
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(eesid="ESP-AP", 
password="protabulesa", authmode=3)
display.set_pixel(5,5,"green")

#client
s = socket.socket()
s.bind(("0.0.0.0",1234))
s.listen(1)

print(f"server running! | IP: {ap.ifconfig()[0]}")

conn, adrr = s.accept()
print(f"{adrr} is connecting")

while True:
    data = conn.recv(1024)
    if not data: break
    print("recieved", data.decode())
if button b.left-ř