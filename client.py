import network
import time
import socket
import ujson

# --- Konfigurace ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_PORT = 1234
WIFI_CONNECT_TIMEOUT_S = 10  # 10 sekund na připojení k Wi-Fi
SOCKET_TIMEOUT_S = 5         # 5 sekund timeout pro síťové operace

def connect_to_wifi(ssid, password, timeout_s):
    """Pokusí se připojit k Wi-Fi síti."""
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    print(f"Připojování k síti '{ssid}'...")
    sta.connect(ssid, password)

    start_time = time.time()
    while not sta.isconnected():
        if time.time() - start_time > timeout_s:
            print("Připojení k Wi-Fi selhalo (timeout).")
            return None
        time.sleep(0.5)
        print("...")

    print(f"Připojeno k Wi-Fi | IP: {sta.ifconfig()[0]}")
    return sta

def communication_loop(sock):
    """Hlavní smyčka pro obousměrnou komunikaci se serverem."""
    # --- Proměnné na straně klienta, které se budou odesílat ---
    client_input = {
        "button_pressed": None,
        "joystick_x": 0,
        "joystick_y": 0,
    }

    # --- Proměnné, které se budou aktualizovat daty ze serveru ---
    # Inicializace s výchozími hodnotami pro případ, že by data nepřišla
    server_state = {
        "list_pp": [],
        "mat_pp": [],
        "toup_pp": {},
        "host_message": ""
    }

    while True:
        # 1. PŘÍJEM DAT ZE SERVERU
        try:
            # Čeká na kompletní řádek (ukončený '\n'), ale s timeoutem
            line = sock.readline()
            if not line:
                print("Server ukončil spojení.")
                break

    s = None
    try:
        # Vytvoření a připojení socketu
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))
        print("Připojeno k serveru!")

        # --- Proměnné na straně klienta, které se budou odesílat ---
        client_input = {
            "button_pressed": None,
            "joystick_x": 0,
            "joystick_y": 0,
        }

        # --- Proměnné, které se budou aktualizovat daty ze serveru ---
        list_pp = []
        mat_pp = []
        toup_pp = {}
        host_message = ""

        # Hlavní komunikační smyčka
        while True:
            # 1. PŘÍJEM DAT ZE SERVERU
            # Server posílá JSON ukončený novým řádkem, readline() je pro to ideální.
            # Blokuje, dokud nepřijme celý řádek.
            line = s.readline()
            if not line:
                # Server ukončil spojení
                print("Server ukončil spojení.")
                break

            try:
                # Dekódování a parsování JSON dat
                server_data = ujson.loads(line)

                # Načtení dat do lokálních proměnných
                list_pp = server_data.get('list_pp', [])
                mat_pp = server_data.get('mat_pp', [])
                toup_pp = server_data.get('toup_pp', {})
                host_message = server_data.get('host_message', '')

                # Vypíše zprávu přijatou od hosta do konzole.
                print(f"Zpráva od hosta: {host_message}")

            except (ValueError, KeyError) as e:
                print(f"Chyba při zpracování JSON od serveru: {e}")
                continue

            # 2. ODESLÁNÍ DAT NA SERVER
            data_to_send = ujson.dumps(client_input) + '\n'
            s.sendall(data_to_send.encode('utf-8'))

    except OSError as e:
        print(f"Chyba spojení: {e}")
    finally:
        if s:
            s.close()
            print("Spojení uzavřeno.")
else:
    print("Připojení k Wi-Fi selhalo :(((((")
