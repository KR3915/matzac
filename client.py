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