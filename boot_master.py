import network
import time 
from logic import *
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP-AP", password="protabulesa", authmode=3)
