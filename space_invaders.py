
import network
import time
import socket
import ujson
import random
from logic import *

# --- Konfigurace ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_IP = "192.168.4.1"
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

# --- Herní stav ---
hrac_X = 5
hrac_Y = 9
enemak_X = 5

strely = []  # Sjednocený seznam všech střel

# --- Buff systém ---
buffy = ["velka_strela", "stit", "klon"]
aktivni_buff = None
buff_timer = 0
hrac_ma_stit = False
klon_aktivni = False
klon_strely_counter = 0

# --- Aktivní buffy na ploše ---
buffy_na_poli = []  # Každý buff: {'x', 'y', 'typ', 'stav'}

# --- Generování buffu na ploše ---
def generuj_buff_na_poli():
    if random.randint(0, 100) == 1:
        typ = random.choice(buffy)
        x = random.randint(0, 9)
        buffy_na_poli.append({'x': x, 'y': 0, 'typ': typ, 'stav': 'modry'})

# --- Update buffů na ploše ---
def update_buffy_na_poli():
    global buffy_na_poli, aktivni_buff
    nove_buffy = []
    for buff in buffy_na_poli:
        # Smazat starou pozici
        display.set_pixel(buff['x'], buff['y'], 'black')
        # Posun dolů, pokud není světle modrý
        if buff['stav'] == 'modry':
            buff['y'] += 1
        # Pokud propadne, zmizí
        if buff['y'] > 9:
            continue
        # Vykreslení barvy
        color = 'blue' if buff['stav'] == 'modry' else 'lightblue'
        display.set_pixel(buff['x'], buff['y'], color)
        nove_buffy.append(buff)
    buffy_na_poli = nove_buffy

# --- Sestřelení buffu střelou ---
def kontrola_sestreleni_buffu():
    global buffy_na_poli
    for buff in buffy_na_poli:
        if buff['stav'] == 'modry':
            for strela in strely:
                if strela['typ'] == 'player' and strela['x'] == buff['x'] and strela['y'] == buff['y']:
                    buff['stav'] = 'svetle_modry'
                    # Smazat střelu
                    strela['y'] = -1

# --- Sebrání buffu hráčem ze strany ---
def kontrola_sebrani_buffu():
    global buffy_na_poli, aktivni_buff
    nove_buffy = []
    for buff in buffy_na_poli:
        if buff['stav'] == 'svetle_modry':
            # Hráč je vlevo nebo vpravo vedle buffu a na stejné úrovni
            if (buff['y'] == hrac_Y and (buff['x'] == hrac_X - 1 or buff['x'] == hrac_X + 1)):
                aktivni_buff = buff['typ']
                print(f"Sebral jsi buff: {aktivni_buff}")
                continue  # Buff sebere, už není na ploše
        nove_buffy.append(buff)
    buffy_na_poli = nove_buffy

# --- Náhodné získání buffu ---
def nahodny_buff():
    global aktivni_buff, buff_timer
    if aktivni_buff is None and random.randint(0, 100) == 1:
        aktivni_buff = random.choice(buffy)
        print(f"Získal jsi buff: {aktivni_buff}")
        # Zde můžete přidat vizuální indikaci buffu

# --- Aktivace buffu ---
def aktivuj_buff():
    global aktivni_buff, buff_timer, hrac_ma_stit, klon_aktivni, klon_strely_counter
    if aktivni_buff == "velka_strela":
        # Velká střela 3x3
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = hrac_X + dx
                y = hrac_Y - 1 + dy
                if 0 <= x <= 9 and 0 <= y <= 9:
                    strely.append({"x": x, "y": y, "dx": 0, "dy": -1, "typ": "player"})
        aktivni_buff = None
    elif aktivni_buff == "stit":
        hrac_ma_stit = True
        buff_timer = time.ticks_ms()
        aktivni_buff = None
    elif aktivni_buff == "klon":
        klon_aktivni = True
        klon_strely_counter = 0
        buff_timer = time.ticks_ms()
        aktivni_buff = None

# --- Update štítu a klonu ---
def update_buff_stavy():
    global hrac_ma_stit, klon_aktivni, buff_timer
    if hrac_ma_stit and time.ticks_diff(time.ticks_ms(), buff_timer) > 3000:
        hrac_ma_stit = False
    if klon_aktivni and time.ticks_diff(time.ticks_ms(), buff_timer) > 5000:
        klon_aktivni = False

# --- Pohyb hráče ---
def pohyb_hrace():
    global hrac_X, strely, klon_strely_counter
    if buttons_a.left:
        hrac_X = max(0, hrac_X - 1)
    elif buttons_a.right:
        hrac_X = min(9, hrac_X + 1)
    if buttons_a.down:
        # Výstřel hráče
        nova_strela = {"x": hrac_X, "y": hrac_Y - 1, "dx": 0, "dy": -1, "typ": "player"}
        strely.append(nova_strela)
        # Klon střílí každou druhou střelu
        if klon_aktivni:
            klon_strely_counter += 1
            if klon_strely_counter % 2 == 0:
                klon_x = min(9, max(0, hrac_X + 2))  # Klon je 2 vpravo, pokud je místo
                strely.append({"x": klon_x, "y": hrac_Y - 1, "dx": 0, "dy": -1, "typ": "player"})
    elif buttons_a.up:
        # Pokus o odražení nepřátelské střely přímo nad hráčem
        for s in strely:
            if s["typ"] == "enemy" and s["x"] == hrac_X and s["y"] == hrac_Y - 1:
                s["typ"] = "reflected"
                s["dy"] = -1
                break
    # Aktivace buffu spodním tlačítkem
    if buttons_a.enter and aktivni_buff:
        aktivuj_buff()

# --- Update všech střel ---
def update_strely():
    global strely
    nove_strely = []
    for strela in strely:
        display.set_pixel(strela["x"], strela["y"], "black")
        strela["x"] += strela.get("dx", 0)
        strela["y"] += strela.get("dy", 0)
        # Kontrola, zda je střela stále na herním poli
        if 0 <= strela["x"] <= 9 and 0 <= strela["y"] <= 9:
            # Kolize s enemákem
            if strela["typ"] in ("player", "reflected") and strela["x"] == enemak_X and strela["y"] == 0:
                enemak_smrt()
                continue
            # Kolize s hráčem
            if strela["typ"] == "enemy" and strela["x"] == hrac_X and strela["y"] == hrac_Y:
                if not hrac_ma_stit:
                    prohra()
                    continue
            # Vykreslení střely podle typu
            if strela["typ"] == "player":
                display.set_pixel(strela["x"], strela["y"], "red")
            elif strela["typ"] == "enemy":
                display.set_pixel(strela["x"], strela["y"], "orange")
            elif strela["typ"] == "reflected":
                display.set_pixel(strela["x"], strela["y"], "blue")
            nove_strely.append(strela)
    strely = nove_strely

# --- Střelba enemáka ---
def enemy_vystrel():
    strely.append({"x": enemak_X, "y": 1, "dx": 0, "dy": 1, "typ": "enemy"})

# --- Flashbang & Laser ---
def flashbang():
    for d in range(10):
        for c in range(10):
            display.set_pixel(c, d, "white")
    time.sleep_ms(1000)
    display.clear()

def laser():
    for y in range(10):
        display.set_pixel(hrac_X, y, "red")
        time.sleep_ms(50)
    for y in range(10):
        display.set_pixel(hrac_X, y, "black")

# --- Pohyb enemáka ---
def pohyb_enemaka():
    global enemak_X
    g = [-1, 0, 0, 0, 0, 0, 0, 1]
    e = g[random.randint(0,7)]
    if enemak_X == 0 and e == -1:
        pass
    elif enemak_X == 9 and e == 1:
        pass
    else:
        display.set_pixel(enemak_X, 0, "black")
        enemak_X += e
    display.set_pixel(enemak_X, 0, "orange")

# --- Smrt enemáka ---
def enemak_smrt():
    for i in range(10):
        display.set_pixel(i, 0, "black")
    display.set_pixel(enemak_X, 0, "red")
    time.sleep_ms(500)
    prohra()

# --- Prohra ---
def prohra():
    while True:
        display.set_pixel(hrac_X, hrac_Y, "red")
        time.sleep_ms(500)
        display.set_pixel(hrac_X, hrac_Y, "black")
        time.sleep_ms(500)
        if buttons_a.enter:
            display.clear()
            return

# --- Hlavní smyčka hry ---
while True:
    pohyb_hrace()
    if buttons_b.enter:
        flashbang()
    if buttons_b.up:
        laser()

    pohyb_enemaka()

    if random.randint(0, 10) == 1:
        enemy_vystrel()

    update_strely()
    update_buff_stavy()
    nahodny_buff()
    generuj_buff_na_poli()
    update_buffy_na_poli()
    kontrola_sestreleni_buffu()
    kontrola_sebrani_buffu()
    time.sleep_ms(100)

# --- Wi-Fi a server ---
if connect_to_wifi(WIFI_SSID, WIFI_PASS, WIFI_CONNECT_TIMEOUT_S):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SOCKET_TIMEOUT_S)
        s.connect((SERVER_IP, SERVER_PORT))
        print("Připojeno k serveru!")

        while True:
            try:
                line = s.readline()
                if not line:
                    print("Server ukončil spojení.")
                    break

                server_data = ujson.loads(line)
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

            user_input = input("Zadejte zprávu pro hosta: ")
            data_to_send = {"user_input": user_input}
            serialized_data = ujson.dumps(data_to_send) + '\n'
            s.sendall(serialized_data.encode("utf-8"))
            time.sleep(0.5)
    except OSError as e:
        print(f"Chyba spojení: {e}")
    finally:
        if s:
            s.close()
            print("Spojení uzavřeno.")
else:
    print("Připojení k Wi-Fi selhalo :(")