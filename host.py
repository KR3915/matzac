import network
import socket
import ujson
import time
import random
# --- Konfigurace Wi-Fi ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_PORT = 1234
SOCKET_TIMEOUT_S = 5

# --- Síťová inicializace (AP) ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=WIFI_SSID, password=WIFI_PASS, authmode=network.AUTH_WPA2_PSK)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', SERVER_PORT))
s.listen(1)
print(f"Server running! | IP: {ap.ifconfig()[0]}")

# --- Herní proměnné (původní logika) ---
hrac_X = 5
hrac_Y = 9
enemak_X = 5
strela_X = None
strela_Y = None
# ... další proměnné dle původního emzáci.py ...

# --- Hlavní smyčka ---
while True:
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn.settimeout(SOCKET_TIMEOUT_S)
    print(f"Client connected from: {addr}")
    try:
        while True:
            # --- 1. Synchronizace: přijmi stav od klienta ---
            try:
                line = conn.readline()
                if not line:
                    print("Client disconnected.")
                    break
                client_state = ujson.loads(line)
                # Zde načti proměnné od klienta
                hrac2_X = client_state.get('hrac2_X', 5)
                hrac2_Y = client_state.get('hrac2_Y', 0)
                # ... další proměnné ...
            except Exception as e:
                print(f"Chyba při čtení od klienta: {e}")

            # --- Trvalé rozsvícení červeného pixelu na pozici druhého hráče ---
            display.set_pixel(hrac2_X, hrac2_Y, "red")

            # --- 2. Herní logika (původní kód z emzáci.py) ---
            from logic import *
            import random
            import time
            # Původní proměnné už jsou nahoře
            def hrac_do_leva() :
                global hrac_X
                time.sleep_ms(100)
                display.set_pixel(hrac_X, hrac_Y, "black")
                hrac_X = hrac_X - 1
                display.set_pixel(hrac_X, hrac_Y, "green")
                return

            def hrac_do_prava() :
                global hrac_X
                time.sleep_ms(100)
                display.set_pixel(hrac_X, hrac_Y, "black")
                hrac_X = hrac_X + 1
                display.set_pixel(hrac_X, hrac_Y, "green")
                return

            def hrac_vystrel() :
                global strela_X
                global strela_Y
                strela_X = hrac_X
                strela_Y = hrac_Y
                for strela_Y in range(10):
                    display.set_pixel(strela_X, 9-strela_Y, "red")
                    display.set_pixel(hrac_X, hrac_Y, "green")
                    time.sleep_ms(100)   
                    if buttons_a.left and hrac_X > 0:
                        hrac_do_leva()
                    if buttons_a.right and hrac_X < 9:
                        hrac_do_prava()
                    pohyb_enemaka()
                    enemak_smrt()
                    display.set_pixel(strela_X, 9-strela_Y, "black")

            def flashbang() :
                c = 0
                d = 0
                for d in range(10):
                    for c in range(10):
                        display.set_pixel(c, d, "white")
                time.sleep_ms(1000)
                display.clear()

            def laser() :
                global strela_X
                global strela_Y
                strela_X = hrac_X
                strela_Y = hrac_Y
                for strela_Y in range(10):
                    display.set_pixel(strela_X, 9-strela_Y, "red")
                    display.set_pixel(hrac_X, hrac_Y, "green")
                    time.sleep_ms(100)   
                    if buttons_a.left and hrac_X > 0:
                        hrac_do_leva()
                    if buttons_a.right and hrac_X < 9:
                        hrac_do_prava()
                    pohyb_enemaka()
                    enemak_smrt()
                for strela_Y in range(10):
                    display.set_pixel(strela_X, 9-strela_Y, "black")
                    display.set_pixel(hrac_X, hrac_Y, "green")
                    time.sleep_ms(100)   
                    if buttons_a.left and hrac_X > 0:
                        hrac_do_leva()
                    if buttons_a.right and hrac_X < 9:
                        hrac_do_prava()
                    pohyb_enemaka()
                    if enemak_X == strela_X :
                        d = 0
                        c = 0
                        for i in range(9):
                            d += 1
                            if strela_X - d > -1 :
                                display.set_pixel(strela_X - d + 1, c, "black")
                                display.set_pixel(strela_X - d, c, "red")
                            if strela_X + d < 10 :
                                display.set_pixel(strela_X + d - 1, c, "black")
                                display.set_pixel(strela_X + d, c, "red")
                            i = i + 1
                            time.sleep_ms(200)
                        display.set_pixel(0, c, "black")
                        display.set_pixel(9, c, "black")
                        prohra()
                        return()

            def strileni_enemaka() :
                x = enemak_X
                y = 9
                for y in range(10):
                    display.set_pixel(x, y, "red")
                    display.set_pixel(enemak_X, 0, "orange")
                    display.set_pixel(hrac_X, hrac_Y, "green")
                    time.sleep_ms(100)
                    if buttons_a.left and hrac_X > 0:
                        hrac_do_leva()
                    if buttons_a.right and hrac_X < 9:
                        hrac_do_prava() 
                    display.set_pixel(x, y, "black")       
                if enemak_X == hrac_X and y == 9 :
                    c = 9
                    d = 0
                    for i in range(9):
                        d += 1
                        if x - d > -1 :
                            display.set_pixel(x - d + 1, c, "black")
                            display.set_pixel(x - d, c, "red")
                        if x + d < 10 :
                            display.set_pixel(x + d - 1, c, "black")
                            display.set_pixel(x + d, c, "red")
                        i = i + 1
                        time.sleep_ms(200)
                    display.set_pixel(0, c, "black")
                    display.set_pixel(9, c, "black")
                    prohra()

            def pohyb_enemaka():
                global enemak_X
                g = [-1, 0, 0, 0, 0, 0, 0, 1]
                e = g[random.randint(0,7)]
                if enemak_X == 0 and e == -1:
                    display.set_pixel(enemak_X, 0, "orange")
                elif enemak_X == 9 and e == 1:
                    display.set_pixel(enemak_X, 0, "orange")
                else :
                    display.set_pixel(enemak_X, 0, "black")
                    enemak_X = enemak_X + e
                    display.set_pixel(enemak_X, 0, "orange")
                    time.sleep_ms(100)

            def enemak_smrt() :
                global strela_Y
                global strela_X
                global enemak_X
                if strela_X == enemak_X and strela_Y == 9 :
                    print("ahoj")
                    d = 0
                    c = 0
                    for i in range(9):
                        d += 1
                        if strela_X - d > -1 :
                            display.set_pixel(strela_X - d + 1, c, "black")
                            display.set_pixel(strela_X - d, c, "red")
                        if strela_X + d < 10 :
                            display.set_pixel(strela_X + d - 1, c, "black")
                            display.set_pixel(strela_X + d, c, "red")
                        i = i + 1
                        time.sleep_ms(200)
                    display.set_pixel(0, c, "black")
                    display.set_pixel(9, c, "black")
                    prohra()

            def prohra() :
                while True :
                    if buttons_a.enter :
                        display.clear()
                        return ()

            # Hlavní smyčka hry
            if buttons_a.left and hrac_X > 0:
                hrac_do_leva()
            if buttons_a.right and hrac_X < 9:
                hrac_do_prava()
            if buttons_a.enter:
                hrac_vystrel()
            if buttons_b.enter:
                flashbang()
            pohyb_enemaka()
            p = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            if p[random.randint(0, 10)] == 1:
                strileni_enemaka()
            if buttons_b.up :
                laser()

            # --- 3. Synchronizace: odešli stav hostitele klientovi ---
            state_to_send = {
                'hrac_X': hrac_X,
                'hrac_Y': hrac_Y,
                'enemak_X': enemak_X,
                'strela_X': strela_X,
                'strela_Y': strela_Y,
                # ... další proměnné ...
            }
            try:
                conn.sendall((ujson.dumps(state_to_send) + '\n').encode('utf-8'))
            except Exception as e:
                print(f"Chyba při odesílání klientovi: {e}")
            time.sleep(0.05)
    finally:
        conn.close()
        print("Connection closed.")
# ... zbytek původního kódu zůstává ...
