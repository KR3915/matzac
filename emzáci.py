import network
import time
import socket
import ujson

# --- Konfigurace ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_IP = "192.168.4.1" # Tuto IP adresu získejte z host.py po spuštění
SERVER_PORT = 1234
WIFI_CONNECT_TIMEOUT_S = 10
SOCKET_TIMEOUT_S = 5

def connect_to_wifi(ssid, password, timeout_s):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print(f"Připojování k síti '{ssid}'...")
    sta.connect(ssid, password)
    start_time = time.time()
    while not sta.isconnected():
        if time.time() - start_time > timeout_s:
            print("Připojení k Wi-Fi selhalo (timeout).")
            sta.active(False)
            return None
        time.sleep(0.5)
        print("...")
    print(f"Připojeno k Wi-Fi | IP: {sta.ifconfig()[0]}")
    return sta
#
from logic import *
import random
import time
hrac1_X = 5
hrac1_Y = 9
enemak_X = 5
strela1_Y = 9
strela1_X = 5

def hrac1_do_leva() :
    global hrac1_X
    time.sleep_ms(100)
    display.set_pixel(hrac1_X, hrac1_Y, "black")
    hrac1_X = hrac1_X - 1
    display.set_pixel(hrac1_X, hrac1_Y, "green")
    return

def hrac1_do_prava() :
    global hrac1_X
    time.sleep_ms(100)
    display.set_pixel(hrac1_X, hrac1_Y, "black")
    hrac1_X = hrac1_X + 1
    display.set_pixel(hrac1_X, hrac1_Y, "green")
    return

def hrac1_vystrel() :
    global strela1_X
    global strela1_Y
    strela1_Y = hrac1_Y
    strela1_X = hrac1_X
    for strela1_Y in range(9,-1,-1):
        display.set_pixel(strela1_X, strela1_Y, "red")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(100)   

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        p = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        if p[random.randint(0, 10)] == 1:
            global enemak_strela_X
            global enemak_X
            global enemak_strela_Y
            enemak_strela_X = enemak_X
            enemak_strela_Y = 1
            strileni_soucasne()
            enemak_strela_Y = 0
            strela1_Y = 1
            return ()
        
        pohyb_enemaka()
        enemak_smrt()

        display.set_pixel(strela1_X, strela1_Y, "black")
    strela1_Y = 1



def flashbang() :
    c = 0
    d = 0
    for d in range(10):
        for c in range(10):
            display.set_pixel(c, d, "white")
    time.sleep_ms(1000)
    display.clear()

def laser() :
    global strela1_X
    global strela1_Y
    strela1_X = hrac1_X
    strela1_Y = hrac1_Y
    for strela1_Y in range(10):
        display.set_pixel(strela1_X, 9-strela1_Y, "red")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(100)   

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        pohyb_enemaka()
    
    enemak_smrt()

    for strela1_Y in range(10):
        display.set_pixel(strela1_X, 9-strela1_Y, "black")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(100)   

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()
        
        pohyb_enemaka()

        if enemak_X == strela1_X :
            d = 0
            c = 0
            for i in range(9):
                d += 1
                if strela1_X - d > -1 :
                    display.set_pixel(strela1_X - d + 1, c, "black")
                    display.set_pixel(strela1_X - d, c, "red")
                if strela1_X + d < 10 :
                    display.set_pixel(strela1_X + d - 1, c, "black")
                    display.set_pixel(strela1_X + d, c, "red")
                i = i + 1
                time.sleep_ms(200)
            display.set_pixel(0, c, "black")
            display.set_pixel(9, c, "black")
            prohra()
            strela1_Y = 5
            return()

def strileni_soucasne() :
    global enemak_strela_Y
    global enemak_strela_X
    global strela1_Y
    global strela1_X
    display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
    display.set_pixel(strela1_X, strela1_Y, "black")
    i = 0
    c = 0
    d = 0
    for i in range(9) :
        if strela1_Y > 0 :
            strela1_Y -= 1
            display.set_pixel(strela1_X, strela1_Y, "red") 
            enemak_smrt()   

        if enemak_strela_Y < 9 :
            enemak_strela_Y += 1
            display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
            hrac1_smrt()
        
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        display.set_pixel(enemak_X, 0, "orange")

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()
        
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        pohyb_enemaka()

        time.sleep_ms(100)
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
        display.set_pixel(strela1_X, strela1_Y, "black")
    time.sleep_ms(100)
    return()


def strileni_enemaka() :
    global enemak_strela_Y
    global enemak_strela_X
    enemak_strela_X = enemak_X
    enemak_strela_Y = 9
    global strela1_Y
    global strela1_X
    for enemak_strela_Y in range(10):
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
        display.set_pixel(enemak_X, 0, "orange")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(100)

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava() 

        pohyb_enemaka()
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")

        if buttons_a.enter:
            strela1_X = hrac1_X
            strela1_Y = 9
            strileni_soucasne()
            enemak_strela_Y = 0
            strela1_Y = 1
            return ()
        hrac1_smrt()

    enemak_strela_Y = 0



       
def hrac1_smrt() :
    global enemak_strela_X
    global enemak_strela_Y
    global hrac1_X
    if enemak_strela_X == hrac1_X and enemak_strela_Y == 9 :
        c = 9
        d = 0
        for i in range(9):
            d += 1
            if enemak_strela_X - d > -1 :
                display.set_pixel(enemak_strela_X - d + 1, c, "black")
                display.set_pixel(enemak_strela_X - d, c, "red")
            if enemak_strela_X + d < 10 :
                display.set_pixel(enemak_strela_X + d - 1, c, "black")
                display.set_pixel(enemak_strela_X + d, c, "red")
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
    global strela1_Y
    global strela1_X
    global enemak_X
    if strela1_X == enemak_X and strela1_Y == 0 :
        d = 0
        c = 0
        for i in range(9):
            d += 1
            if strela1_X - d > -1 :
                display.set_pixel(strela1_X - d + 1, c, "black")
                display.set_pixel(strela1_X - d, c, "red")
            if strela1_X + d < 10 :
                display.set_pixel(strela1_X + d - 1, c, "black")
                display.set_pixel(strela1_X + d, c, "red")
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

while True:
    if buttons_a.left and hrac1_X > 0:
        hrac1_do_leva()

    if buttons_a.right and hrac1_X < 9:
       hrac1_do_prava()     

    if buttons_a.enter:
        hrac1_vystrel()
    
    if buttons_b.enter:
        flashbang()

    pohyb_enemaka()

    p = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    if p[random.randint(0, 10)] == 1:
        strileni_enemaka()
    
    if buttons_b.up :
        laser()


#
# --- Hlavní skript ---
if connect_to_wifi(WIFI_SSID, WIFI_PASS, WIFI_CONNECT_TIMEOUT_S):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SOCKET_TIMEOUT_S)
        s.connect((SERVER_IP, SERVER_PORT))
        print("Připojeno k serveru!")

        # Hlavní komunikační smyčka
        while True:
            # 1. PŘÍJEM DAT ZE SERVERU
            try:
                line = s.readline()
                if not line:
                    print("Server ukončil spojení.")
                    break
                
                server_data = ujson.loads(line)
                
                # Zobrazení dat na konzoli
                print("--- Přijato ze serveru ---")
                print(f"list_pp: {server_data.get('list_pp')}")
                print(f"host_message: {server_data.get('host_message')}")
                print(f"server_processed_input: {server_data.get('received_client_input')}")
                print("--------------------------")
            
            except (ValueError, KeyError) as e:
                print(f"Chyba při zpracování JSON od serveru: {e}")
                continue
            except OSError as e:
                print(f"Chyba při čtení ze socketu (timeout): {e}")
                continue

            # 2. ODESLÁNÍ DAT NA SERVER
            # Příklad s uživatelským vstupem z konzole.
            # V reálné aplikaci by to byl vstup z tlačítek, joysticku atd.
            user_input = input("Zadejte zprávu pro hosta: ")
            
            data_to_send = {
                "user_input": user_input
            }
            
            serialized_data = ujson.dumps(data_to_send) + '\n'
            s.sendall(serialized_data.encode('utf-8'))
            
            time.sleep(0.5) # Krátká pauza
            
    except OSError as e:
        print(f"Chyba spojení: {e}")
    finally:
        if s:
            s.close()
            print("Spojení uzavřeno.")
else:
    print("Připojení k Wi-Fi selhalo :(")
