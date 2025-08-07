import network
import time
import socket
import ujson
from game_logic import GameState

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

# --- Hlavní skript ---
if connect_to_wifi(WIFI_SSID, WIFI_PASS, WIFI_CONNECT_TIMEOUT_S):
    s = None
    game = GameState()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SOCKET_TIMEOUT_S)
        s.connect((SERVER_IP, SERVER_PORT))
        print("Připojeno k serveru!")

        while True:
            # 1. Handle local (client) input
            # Replace this with real input handling for your hardware
            client_action = input("Client action (left/right/shoot/none): ")
            msg = ujson.dumps({'action': client_action}) + '\n'
            s.sendall(msg.encode('utf-8'))

            # 2. Receive updated game state from host
            try:
                line = s.readline()
                if not line:
                    print("Server ukončil spojení.")
                    break
                state = ujson.loads(line)
                game.from_dict(state)
                # game.render()  # Implement for your display
                print(f"Game state: {game.to_dict()}")
            except Exception as e:
                print(f"Chyba při zpracování stavu hry od serveru: {e}")
                continue
            time.sleep(0.1)
    except OSError as e:
        print(f"Chyba spojení: {e}")
    finally:
        if s:
            s.close()
            print("Spojení uzavřeno.")
else:
    print("Připojení k Wi-Fi selhalo :(")