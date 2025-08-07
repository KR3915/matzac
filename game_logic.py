import random
import time

class GameState:
    def __init__(self):
        # Player 1 (host) and Player 2 (client) positions
        self.players = {
            'host': {'x': 5, 'y': 9, 'alive': True, 'shot': None},
            'client': {'x': 5, 'y': 0, 'alive': True, 'shot': None}
        }
        self.enemy = {'x': 5, 'alive': True}
        self.last_action = {'host': None, 'client': None}
        self.flashbang = False
        self.laser = False
        self.display = None  # Should be set to the display object

    def set_display(self, display):
        self.display = display

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
        # Shot travels vertically (host: up, client: down)
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
        # Move shots and check for hits
        for player in self.players:
            shot = self.players[player]['shot']
            if shot and len(shot) > 0:
                x, y = shot.pop(0)
                # Check for enemy hit
                if self.enemy['alive'] and x == self.enemy['x'] and ((player == 'host' and y == 0) or (player == 'client' and y == 9)):
                    self.enemy['alive'] = False
                # Check for player hit (friendly fire off)
                # Optionally, check for other player
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

    def render(self):
        # This should update the display based on the current state
        # Needs to be implemented for your hardware
        pass
