import random
import time

class Shot:
    def __init__(self, x, y, direction, owner):
        self.x = x
        self.y = y
        self.direction = direction  # -1 for up, 1 for down
        self.owner = owner  # 'host', 'client', or 'enemy'
        self.active = True

class GameState:
    def __init__(self):
        # Player 1 (host) and Player 2 (client) positions
        self.players = {
            'host': {'x': 5, 'y': 9, 'alive': True, 'shots_remaining': 5},
            'client': {'x': 5, 'y': 0, 'alive': True, 'shots_remaining': 5}
        }
        self.enemy = {'x': 5, 'alive': True}
        self.last_action = {'host': None, 'client': None}
        self.flashbang = False
        self.laser = False
        self.display = None  # Should be set to the display object
        
        # Shot management
        self.active_shots = []  # List of Shot objects
        self.max_player_shots = 5
        self.enemy_shot_cooldown = 0
        self.enemy_shot_delay = 30  # Frames between enemy shots

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
        if self.players[player]['shots_remaining'] <= 0:
            return  # No shots remaining
        
        # Create new shot
        x = self.players[player]['x']
        y = self.players[player]['y']
        direction = -1 if player == 'host' else 1
        
        new_shot = Shot(x, y, direction, player)
        self.active_shots.append(new_shot)
        
        # Decrease shot count
        self.players[player]['shots_remaining'] -= 1
        self.last_action[player] = 'shoot'

    def enemy_shoot(self):
        if not self.enemy['alive']:
            return
        
        # Random chance to shoot
        if random.randint(1, 100) <= 5:  # 5% chance per frame
            x = self.enemy['x']
            y = 0
            direction = 1  # Enemy shoots down
            
            new_shot = Shot(x, y, direction, 'enemy')
            self.active_shots.append(new_shot)

    def update_shots(self):
        # Move all active shots
        shots_to_remove = []
        
        for shot in self.active_shots:
            if not shot.active:
                shots_to_remove.append(shot)
                continue
                
            # Move shot
            shot.y += shot.direction
            
            # Check if shot is out of bounds
            if shot.y < 0 or shot.y > 9:
                shot.active = False
                shots_to_remove.append(shot)
                continue
            
            # Check for hits
            if self.check_shot_hits(shot):
                shot.active = False
                shots_to_remove.append(shot)
                continue
        
        # Remove inactive shots
        for shot in shots_to_remove:
            if shot in self.active_shots:
                self.active_shots.remove(shot)
                
        # Replenish player shots over time
        for player in self.players:
            if self.players[player]['shots_remaining'] < self.max_player_shots:
                # Replenish 1 shot every 100 frames (about 5 seconds)
                if random.randint(1, 100) <= 1:
                    self.players[player]['shots_remaining'] += 1

    def check_shot_hits(self, shot):
        # Check if shot hits enemy
        if shot.owner in ['host', 'client'] and self.enemy['alive']:
            if shot.x == self.enemy['x'] and shot.y == 0:
                self.enemy['alive'] = False
                return True
        
        # Check if enemy shot hits players
        if shot.owner == 'enemy':
            for player, player_data in self.players.items():
                if player_data['alive']:
                    if shot.x == player_data['x'] and shot.y == player_data['y']:
                        player_data['alive'] = False
                        return True
        
        return False

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

    def get_shot_count(self, player):
        """Get current number of active shots for a player"""
        count = 0
        for shot in self.active_shots:
            if shot.owner == player:
                count += 1
        return count

    def to_dict(self):
        return {
            'players': self.players,
            'enemy': self.enemy,
            'flashbang': self.flashbang,
            'laser': self.laser,
            'active_shots': [(shot.x, shot.y, shot.direction, shot.owner) for shot in self.active_shots]
        }

    def from_dict(self, data):
        self.players = data['players']
        self.enemy = data['enemy']
        self.flashbang = data.get('flashbang', False)
        self.laser = data.get('laser', False)
        
        # Reconstruct shots
        self.active_shots = []
        for shot_data in data.get('active_shots', []):
            x, y, direction, owner = shot_data
            shot = Shot(x, y, direction, owner)
            self.active_shots.append(shot)

    def render(self):
        # This should update the display based on the current state
        # Needs to be implemented for your hardware
        pass
