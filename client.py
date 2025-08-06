import network
import time
import socket
import ujson

sta = network.WLAN(network.STA_IF) #station
sta.active(True)

#pripojit k ESP
sta.connect("ESP-AP", "protabulesa")

for _ in range(20):
    if sta.isconnected():
        break
    print("čekání na připojení...")
    time.sleep(0.5)

if sta.isconnected():
    # Gateway je IP adresa Access Pointu (serveru)
    server_ip = sta.ifconfig()[2]
    server_port = 1234
    print(f"Připojeno k Wi-Fi | IP: {sta.ifconfig()[0]}")
    print(f"Pokouším se připojit k serveru na {server_ip}:{server_port}...")

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

                # Pro ukázku vypíšeme část přijatých dat
                print(f"Přijato: {toup_pp}")

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
