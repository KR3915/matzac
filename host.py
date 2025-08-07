import network
import socket
import ujson
import time
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

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP-AP", password="protabulesa", authmode=network.AUTH_WPA2_PSK)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))
s.listen(1)

print(f"Server running! | IP: {ap.ifconfig()[0]}")

game = GameState()

while True:
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn.settimeout(5.0)
    print(f"Client connected from: {addr}")

    try:
        while True:
            # 1. Receive client action
            try:
                line = conn.readline()
                if not line:
                    print("Client disconnected gracefully.")
                    break
                client_msg = ujson.loads(line)
                client_action = client_msg.get('action')
            except Exception as e:
                print(f"Error receiving client action: {e}")
                client_action = None

            # 2. Handle local (host) input
            host_action = input("Host action (left/right/shoot/none): ")
            if host_action == 'left':
                game.move_player('host', 'left')
            elif host_action == 'right':
                game.move_player('host', 'right')
            elif host_action == 'shoot':
                game.player_shoot('host')

            # 3. Apply client action
            if client_action == 'left':
                game.move_player('client', 'left')
            elif client_action == 'right':
                game.move_player('client', 'right')
            elif client_action == 'shoot':
                game.player_shoot('client')

            # 4. Update game state
            game.update_shots()
            game.move_enemy()

            # 5. Send updated state to client
            state_to_send = ujson.dumps(game.to_dict()) + '\n'
            conn.sendall(state_to_send.encode('utf-8'))
            time.sleep(0.1)

    except OSError as e:
        print(f"Connection with {addr} lost: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed. Ready for next client.")
