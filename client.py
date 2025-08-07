import network
import time
import socket
import ujson
import random

class GameState:
    def __init__(self):
        self.players = {
            'host': {'x': 5, 'y': 9, 'alive': True, 'shot': None},
            'client': {'x': 5, 'y': 0, 'alive': True, 'shot': None}
        }
        self.enemy = {'x': 5, 'alive': True}
        self.last_action = {'host': None, 'client': None}
        self.flashbang = False
        self.laser = False
        self.display = None

    def move_player(self, player, direction):
        if not self.players[player]['alive']:
            return
        if direction == 'left' and self.players[player]['x'] > 0:
            self.players[player]['x'] -= 1
        elif direction == 'right' and self.players[player]['x'] < 9:
            self.players[player]['x'] += 1
        self.last_action[player] = f'move_{direction}'

    def player_shoot(self, player):
        if not self.players[player]['alive']:
            return
        x = self.players[player]['x']
        y = self.players[player]['y']
        direction = -1 if player == 'host' else 1
        shot_path = []
        for i in range(10):
            ny = y + i * direction
            if 0 <= ny < 10:
                shot_path.append((x, ny))
        self.players[player]['shot'] = shot_path
        self.last_action[player] = 'shoot'

    def update_shots(self):
        for player in self.players:
            shot = self.players[player]['shot']
            if shot and len(shot) > 0:
                x, y = shot.pop(0)
                if self.enemy['alive'] and x == self.enemy['x'] and ((player == 'host' and y == 0) or (player == 'client' and y == 9)):
                    self.enemy['alive'] = False
                self.players[player]['shot'] = shot if len(shot) > 0 else None

    def move_enemy(self):
        if not self.enemy['alive']:
            return
        g = [-1, 0, 0, 0, 0, 0, 0, 1]
        e = g[random.randint(0, 7)]
        if self.enemy['x'] == 0 and e == -1:
            pass
        elif self.enemy['x'] == 9 and e == 1:
            pass
        else:
            self.enemy['x'] += e

    def to_dict(self):
        return {
            'players': self.players,
            'enemy': self.enemy,
            'flashbang': self.flashbang,
            'laser': self.laser
        }

    def from_dict(self, data):
        self.players = data['players']
        self.enemy = data['enemy']
        self.flashbang = data.get('flashbang', False)
        self.laser = data.get('laser', False)

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
