import network
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(eesid="test_net", 
password="1234", authmode=3)

