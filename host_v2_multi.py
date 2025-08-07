import network
import socket
import ujson
import time
import random

# --- Konfigurace Wi-Fi ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_PORT = 1234
SOCKET_TIMEOUT_S = 5

# --- Herní konstanty ---
DISPLAY_WIDTH = 10
DISPLAY_HEIGHT = 20
PLAYER_START_X = 5
PLAYER_START_Y = 18  # Host hraje dole
CLIENT_START_Y = 1   # Klient hraje nahoře
MAX_SHOTS = 5  # Maximální počet střel najednou

# --- Síťová inicializace (AP) ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=WIFI_SSID, password=WIFI_PASS, authmode=network.AUTH_WPA2_PSK)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', SERVER_PORT))
s.listen(1)
print(f"Server running! | IP: {ap.ifconfig()[0]}")

# --- Herní stav ---
class GameState:
    def __init__(self):
        # Host (dole)
        self.host_x = PLAYER_START_X
        self.host_y = PLAYER_START_Y
        self.host_alive = True
        self.host_shots = []  # Seznam střel hosta
        
        # Klient (nahoře)
        self.client_x = PLAYER_START_X
        self.client_y = CLIENT_START_Y
        self.client_alive = True
        self.client_shots = []  # Seznam střel klienta
        
        # Nepřátelé
        self.enemies = []
        self.init_enemies()
        
        # Skóre
        self.host_score = 0
        self.client_score = 0
        
        # Herní stav
        self.game_over = False
        self.winner = None

    def init_enemies(self):
        self.enemies = []
        # Vytvoříme nepřátele v horní části obrazovky (řádky 0-8)
        for row in range(3):
            for col in range(8):
                if col < DISPLAY_WIDTH:
                    self.enemies.append({
                        'x': col + 1,
                        'y': row + 1,
                        'alive': True
                    })

    def move_host(self, direction):
        if not self.host_alive:
            return
        if direction == 'left' and self.host_x > 0:
            self.host_x -= 1
        elif direction == 'right' and self.host_x < DISPLAY_WIDTH - 1:
            self.host_x += 1

    def move_client(self, direction):
        if not self.client_alive:
            return
        if direction == 'left' and self.client_x > 0:
            self.client_x -= 1
        elif direction == 'right' and self.client_x < DISPLAY_WIDTH - 1:
            self.client_x += 1

    def host_shoot(self):
        if not self.host_alive or len(self.host_shots) >= MAX_SHOTS:
            return
        # Přidáme novou střelu
        self.host_shots.append({
            'x': self.host_x,
            'y': self.host_y - 1
        })

    def client_shoot(self):
        if not self.client_alive or len(self.client_shots) >= MAX_SHOTS:
            return
        # Přidáme novou střelu
        self.client_shots.append({
            'x': self.client_x,
            'y': self.client_y + 1
        })

    def update_shots(self):
        # Pohyb střel hosta (nahoru)
        shots_to_remove = []
        for i, shot in enumerate(self.host_shots):
            shot['y'] -= 1
            if shot['y'] < 0:
                shots_to_remove.append(i)
            else:
                # Kontrola zásahu nepřátel
                for enemy in self.enemies:
                    if (enemy['alive'] and 
                        enemy['x'] == shot['x'] and 
                        enemy['y'] == shot['y']):
                        enemy['alive'] = False
                        shots_to_remove.append(i)
                        self.host_score += 10
                        break
                # Kontrola zásahu klienta
                if (self.client_alive and 
                    self.client_x == shot['x'] and 
                    self.client_y == shot['y']):
                    self.client_alive = False
                    shots_to_remove.append(i)
        
        # Odstraníme střely, které zasáhly nebo opustily obrazovku
        for i in reversed(shots_to_remove):
            if i < len(self.host_shots):
                self.host_shots.pop(i)

        # Pohyb střel klienta (dolů)
        shots_to_remove = []
        for i, shot in enumerate(self.client_shots):
            shot['y'] += 1
            if shot['y'] >= DISPLAY_HEIGHT:
                shots_to_remove.append(i)
            else:
                # Kontrola zásahu nepřátel
                for enemy in self.enemies:
                    if (enemy['alive'] and 
                        enemy['x'] == shot['x'] and 
                        enemy['y'] == shot['y']):
                        enemy['alive'] = False
                        shots_to_remove.append(i)
                        self.client_score += 10
                        break
                # Kontrola zásahu hosta
                if (self.host_alive and 
                    self.host_x == shot['x'] and 
                    self.host_y == shot['y']):
                    self.host_alive = False
                    shots_to_remove.append(i)
        
        # Odstraníme střely, které zasáhly nebo opustily obrazovku
        for i in reversed(shots_to_remove):
            if i < len(self.client_shots):
                self.client_shots.pop(i)

    def move_enemies(self):
        # Jednoduchý pohyb nepřátel
        for enemy in self.enemies:
            if enemy['alive']:
                # Náhodný pohyb
                if random.randint(0, 10) == 0:
                    direction = random.choice([-1, 0, 1])
                    new_x = enemy['x'] + direction
                    if 0 <= new_x < DISPLAY_WIDTH:
                        enemy['x'] = new_x

    def check_game_over(self):
        # Kontrola, zda jsou všichni nepřátelé mrtví
        alive_enemies = sum(1 for enemy in self.enemies if enemy['alive'])
        if alive_enemies == 0:
            self.game_over = True
            if self.host_score > self.client_score:
                self.winner = "host"
            elif self.client_score > self.host_score:
                self.winner = "client"
            else:
                self.winner = "tie"
        
        # Kontrola, zda jsou oba hráči mrtví
        if not self.host_alive and not self.client_alive:
            self.game_over = True
            self.winner = "enemies"

    def to_dict(self):
        return {
            'host_x': self.host_x,
            'host_y': self.host_y,
            'host_alive': self.host_alive,
            'host_shots': self.host_shots,
            'client_x': self.client_x,
            'client_y': self.client_y,
            'client_alive': self.client_alive,
            'client_shots': self.client_shots,
            'enemies': self.enemies,
            'host_score': self.host_score,
            'client_score': self.client_score,
            'game_over': self.game_over,
            'winner': self.winner
        }

    def from_dict(self, data):
        self.host_x = data.get('host_x', PLAYER_START_X)
        self.host_y = data.get('host_y', PLAYER_START_Y)
        self.host_alive = data.get('host_alive', True)
        self.host_shots = data.get('host_shots', [])
        self.client_x = data.get('client_x', PLAYER_START_X)
        self.client_y = data.get('client_y', CLIENT_START_Y)
        self.client_alive = data.get('client_alive', True)
        self.client_shots = data.get('client_shots', [])
        self.enemies = data.get('enemies', [])
        self.host_score = data.get('host_score', 0)
        self.client_score = data.get('client_score', 0)
        self.game_over = data.get('game_over', False)
        self.winner = data.get('winner')

def render_display(game_state):
    """Vykreslí herní stav na displej"""
    # Vyčistíme displej
    display.clear()
    
    # Vykreslíme hosta (zelený)
    if game_state.host_alive:
        display.set_pixel(game_state.host_x, game_state.host_y, "green")
    
    # Vykreslíme klienta (červený)
    if game_state.client_alive:
        display.set_pixel(game_state.client_x, game_state.client_y, "red")
    
    # Vykreslíme střely hosta (žluté)
    for shot in game_state.host_shots:
        if 0 <= shot['y'] < DISPLAY_HEIGHT:
            display.set_pixel(shot['x'], shot['y'], "yellow")
    
    # Vykreslíme střely klienta (žluté)
    for shot in game_state.client_shots:
        if 0 <= shot['y'] < DISPLAY_HEIGHT:
            display.set_pixel(shot['x'], shot['y'], "yellow")
    
    # Vykreslíme nepřátele (oranžoví)
    for enemy in game_state.enemies:
        if enemy['alive']:
            display.set_pixel(enemy['x'], enemy['y'], "orange")

# --- Hlavní smyčka ---
while True:
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn.settimeout(SOCKET_TIMEOUT_S)
    print(f"Client connected from: {addr}")
    
    # Inicializace hry
    game_state = GameState()
    
    try:
        while True:
            # --- 1. Příjem dat od klienta ---
            try:
                line = conn.readline()
                if not line:
                    print("Client disconnected.")
                    break
                
                client_data = ujson.loads(line)
                print(f"Received from client: {client_data}")
                
                # Aktualizace pozice klienta
                if 'client_x' in client_data:
                    game_state.client_x = client_data['client_x']
                if 'client_y' in client_data:
                    game_state.client_y = client_data['client_y']
                if 'client_shot' in client_data and client_data['client_shot']:
                    game_state.client_shoot()
                
            except Exception as e:
                print(f"Error reading from client: {e}")
            
            # --- 2. Herní logika ---
            # Ovládání hosta
            if buttons_a.left:
                game_state.move_host('left')
            if buttons_a.right:
                game_state.move_host('right')
            if buttons_a.enter:
                game_state.host_shoot()
            
            # Aktualizace střel
            game_state.update_shots()
            
            # Pohyb nepřátel
            game_state.move_enemies()
            
            # Kontrola konce hry
            game_state.check_game_over()
            
            # Vykreslení
            render_display(game_state)
            
            # --- 3. Odeslání dat klientovi ---
            state_to_send = game_state.to_dict()
            try:
                conn.sendall((ujson.dumps(state_to_send) + '\n').encode('utf-8'))
            except Exception as e:
                print(f"Error sending to client: {e}")
            
            # Kontrola konce hry
            if game_state.game_over:
                print(f"Game Over! Winner: {game_state.winner}")
                print(f"Final scores - Host: {game_state.host_score}, Client: {game_state.client_score}")
                break
            
            time.sleep(0.1)  # 10 FPS
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        conn.close()
        print("Connection closed.")
