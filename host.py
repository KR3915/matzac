from game_logic import GameState
import network
import socket
import ujson
import time
import random

class MultiplayerHost:
    def __init__(self, display, buttons_a, buttons_b):
        self.display = display
        self.buttons_a = buttons_a
        self.buttons_b = buttons_b
        self.game_state = GameState()
        self.game_state.set_display(display)
        
        # Network setup
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid="ESP-AP", password="protabulesa", authmode=network.AUTH_WPA2_PSK)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 1234))
        self.socket.listen(1)
        
        print(f"Server running! | IP: {self.ap.ifconfig()[0]}")
        
    def clear_display(self):
        """Clear the entire display"""
        self.display.clear()
        
    def draw_game_state(self):
        """Draw the current game state on display"""
        self.clear_display()
        
        # Draw players
        for player, data in self.game_state.players.items():
            if data['alive']:
                color = "green" if player == 'host' else "blue"
                self.display.set_pixel(data['x'], data['y'], color)
                
        # Draw enemy
        if self.game_state.enemy['alive']:
            self.display.set_pixel(self.game_state.enemy['x'], 0, "orange")
            
        # Draw shots
        for shot in self.game_state.active_shots:
            if shot.active:
                if shot.owner == 'host':
                    color = "red"
                elif shot.owner == 'client':
                    color = "yellow"
                else:  # enemy
                    color = "purple"
                self.display.set_pixel(shot.x, shot.y, color)
                
        # Draw shot counters
        self.draw_shot_counters()
        
    def draw_shot_counters(self):
        """Draw shot counters for both players"""
        # Host shots (left side)
        for i in range(self.game_state.players['host']['shots_remaining']):
            if i < 5:
                self.display.set_pixel(i, 9, "green")
                
        # Client shots (right side)
        for i in range(self.game_state.players['client']['shots_remaining']):
            if i < 5:
                self.display.set_pixel(9-i, 9, "blue")
                
    def handle_input(self):
        """Handle local player input"""
        if self.buttons_a.left:
            self.game_state.move_player('host', 'left')
        if self.buttons_a.right:
            self.game_state.move_player('host', 'right')
        if self.buttons_a.enter:
            self.game_state.player_shoot('host')
        if self.buttons_b.enter:
            self.flashbang()
        if self.buttons_b.up:
            self.laser()
            
    def flashbang(self):
        """Flashbang effect"""
        for y in range(10):
            for x in range(10):
                self.display.set_pixel(x, y, "white")
        time.sleep_ms(1000)
        self.game_state.flashbang = True
        
    def laser(self):
        """Laser weapon - shoots multiple shots"""
        if self.game_state.players['host']['shots_remaining'] < 3:
            return
            
        # Create multiple shots in a line
        for dx in [-1, 0, 1]:
            x = self.game_state.players['host']['x'] + dx
            if 0 <= x <= 9:
                new_shot = Shot(x, self.game_state.players['host']['y'] - 1, -1, 'host')
                self.game_state.active_shots.append(new_shot)
                
        self.game_state.players['host']['shots_remaining'] -= 3
        
    def update_game(self):
        """Update game state"""
        # Move enemy
        self.game_state.move_enemy()
        
        # Enemy shooting
        self.game_state.enemy_shoot()
        
        # Update all shots
        self.game_state.update_shots()
        
        # Check for game over conditions
        alive_players = sum(1 for player in self.game_state.players.values() if player['alive'])
        if alive_players == 0:
            return "game_over"
        elif not self.game_state.enemy['alive']:
            return "victory"
            
        return "continue"
        
    def run_game(self):
        """Main game loop"""
        print("Waiting for client connection...")
        conn, addr = self.socket.accept()
        conn.settimeout(5.0)
        print(f"Client connected from: {addr}")
        
        try:
            while True:
                # Handle local input
                self.handle_input()
                
                # Update game state
                game_status = self.update_game()
                
                # Send game state to client
                game_data = self.game_state.to_dict()
                game_data['game_status'] = game_status
                
                try:
                    serialized_data = ujson.dumps(game_data) + '\n'
                    conn.sendall(serialized_data.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending data: {e}")
                    break
                    
                # Receive client input
                try:
                    line = conn.readline()
                    if not line:
                        print("Client disconnected")
                        break
                        
                    client_data = ujson.loads(line)
                    self.handle_client_input(client_data)
                    
                except Exception as e:
                    print(f"Error receiving client data: {e}")
                    
                # Draw game state
                self.draw_game_state()
                
                # Handle game status
                if game_status == "game_over":
                    self.show_game_over("DEFEAT")
                    break
                elif game_status == "victory":
                    self.show_game_over("VICTORY")
                    break
                    
                time.sleep_ms(100)
                
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            conn.close()
            print("Connection closed")
            
    def handle_client_input(self, client_data):
        """Handle input from client"""
        if 'action' in client_data:
            action = client_data['action']
            if action == 'move_left':
                self.game_state.move_player('client', 'left')
            elif action == 'move_right':
                self.game_state.move_player('client', 'right')
            elif action == 'shoot':
                self.game_state.player_shoot('client')
            elif action == 'flashbang':
                self.game_state.flashbang = True
            elif action == 'laser':
                # Client laser (similar to host)
                if self.game_state.players['client']['shots_remaining'] < 3:
                    return
                for dx in [-1, 0, 1]:
                    x = self.game_state.players['client']['x'] + dx
                    if 0 <= x <= 9:
                        new_shot = Shot(x, self.game_state.players['client']['y'] + 1, 1, 'client')
                        self.game_state.active_shots.append(new_shot)
                self.game_state.players['client']['shots_remaining'] -= 3
                
    def show_game_over(self, message):
        """Show game over screen"""
        self.clear_display()
        
        # Simple text display
        if message == "VICTORY":
            pixels = [(3, 4), (4, 4), (5, 4), (6, 4)]  # WIN
        else:
            pixels = [(2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)]  # DEFEAT
            
        for x, y in pixels:
            self.display.set_pixel(x, y, "red")
            
        time.sleep_ms(3000)
        
# Example usage:
# host = MultiplayerHost(display, buttons_a, buttons_b)
# host.run_game()
