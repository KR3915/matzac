import network
import socket
import ujson
import time
import random

# --- Konfigurace Wi-Fi ---
WIFI_SSID = "ESP-AP"
WIFI_PASS = "protabulesa"
SERVER_IP = "192.168.4.1"
SERVER_PORT = 1234
SOCKET_TIMEOUT_S = 5

# --- Herní konstanty ---
DISPLAY_WIDTH = 10
DISPLAY_HEIGHT = 20
PLAYER_START_X = 5
PLAYER_START_Y = 1   # Klient hraje nahoře

# --- Síťová inicializace (STA) ---
sta = network.WLAN(network.STA_IF)
sta.active(True)
print(f"Připojování k síti '{WIFI_SSID}'...")
sta.connect(WIFI_SSID, WIFI_PASS)
start_time = time.time()
while not sta.isconnected():
    if time.time() - start_time > 10:
        print("Připojení k Wi-Fi selhalo (timeout).")
        sta.active(False)
        raise RuntimeError('Wi-Fi connection failed')
    time.sleep(0.5)
    print("...")
print(f"Připojeno k Wi-Fi | IP: {sta.ifconfig()[0]}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(SOCKET_TIMEOUT_S)
s.connect((SERVER_IP, SERVER_PORT))
print("Připojeno k serveru!")

# --- Herní stav klienta ---
class ClientGameState:
    def __init__(self):
        # Klient (nahoře)
        self.client_x = PLAYER_START_X
        self.client_y = PLAYER_START_Y
        self.client_alive = True
        self.client_shot = False
        
        # Host (dole) - přijímáme od serveru
        self.host_x = PLAYER_START_X
        self.host_y = 18
        self.host_alive = True
        
        # Nepřátelé - přijímáme od serveru
        self.enemies = []
        
        # Skóre
        self.host_score = 0
        self.client_score = 0
        
        # Herní stav
        self.game_over = False
        self.winner = None

    def move_client(self, direction):
        if not self.client_alive:
            return
        if direction == 'left' and self.client_x > 0:
            self.client_x -= 1
        elif direction == 'right' and self.client_x < DISPLAY_WIDTH - 1:
            self.client_x += 1

    def client_shoot(self):
        if not self.client_alive:
            return
        self.client_shot = True

    def to_dict(self):
        return {
            'client_x': self.client_x,
            'client_y': self.client_y,
            'client_shot': self.client_shot
        }

    def from_dict(self, data):
        self.host_x = data.get('host_x', PLAYER_START_X)
        self.host_y = data.get('host_y', 18)
        self.host_alive = data.get('host_alive', True)
        self.enemies = data.get('enemies', [])
        self.host_score = data.get('host_score', 0)
        self.client_score = data.get('client_score', 0)
        self.game_over = data.get('game_over', False)
        self.winner = data.get('winner')

def render_display(game_state):
    """Vykreslí herní stav na displej"""
    # Vyčistíme displej
    display.clear()
    
    # Vykreslíme hosta (zelený) - dole
    if game_state.host_alive:
        display.set_pixel(game_state.host_x, game_state.host_y, "green")
    
    # Vykreslíme klienta (červený) - nahoře
    if game_state.client_alive:
        display.set_pixel(game_state.client_x, game_state.client_y, "red")
    
    # Vykreslíme nepřátele (oranžoví)
    for enemy in game_state.enemies:
        if enemy['alive']:
            display.set_pixel(enemy['x'], enemy['y'], "orange")

# --- Hlavní smyčka ---
game_state = ClientGameState()

try:
    while True:
        # --- 1. Odeslání dat hostiteli ---
        state_to_send = game_state.to_dict()
        try:
            s.sendall((ujson.dumps(state_to_send) + '\n').encode('utf-8'))
        except Exception as e:
            print(f"Chyba při odesílání hostiteli: {e}")
            break

        # --- 2. Příjem dat od hostitele ---
        try:
            line = s.readline()
            if not line:
                print("Hostitel ukončil spojení.")
                break
            
            host_data = ujson.loads(line)
            print(f"Received from host: {host_data}")
            
            # Aktualizace herního stavu
            game_state.from_dict(host_data)
            
        except Exception as e:
            print(f"Chyba při čtení od hostitele: {e}")
            break

        # --- 3. Herní logika ---
        # Ovládání klienta
        if buttons_a.left:
            game_state.move_client('left')
        if buttons_a.right:
            game_state.move_client('right')
        if buttons_a.enter:
            game_state.client_shoot()
        
        # Reset střely po odeslání
        game_state.client_shot = False
        
        # Vykreslení
        render_display(game_state)
        
        # Kontrola konce hry
        if game_state.game_over:
            print(f"Game Over! Winner: {game_state.winner}")
            print(f"Final scores - Host: {game_state.host_score}, Client: {game_state.client_score}")
            
            # Zobrazení výsledku na displeji
            display.clear()
            if game_state.winner == "client":
                # Klient vyhrál - zelená obrazovka
                for x in range(DISPLAY_WIDTH):
                    for y in range(DISPLAY_HEIGHT):
                        display.set_pixel(x, y, "green")
            elif game_state.winner == "host":
                # Host vyhrál - červená obrazovka
                for x in range(DISPLAY_WIDTH):
                    for y in range(DISPLAY_HEIGHT):
                        display.set_pixel(x, y, "red")
            elif game_state.winner == "tie":
                # Remíza - žlutá obrazovka
                for x in range(DISPLAY_WIDTH):
                    for y in range(DISPLAY_HEIGHT):
                        display.set_pixel(x, y, "yellow")
            else:
                # Nepřátelé vyhráli - oranžová obrazovka
                for x in range(DISPLAY_WIDTH):
                    for y in range(DISPLAY_HEIGHT):
                        display.set_pixel(x, y, "orange")
            
            # Čekání na restart
            while True:
                if buttons_a.enter:
                    # Restart hry
                    game_state = ClientGameState()
                    break
                time.sleep(0.1)
        
        time.sleep(0.1)  # 10 FPS

except Exception as e:
    print(f"Connection error: {e}")
finally:
    s.close()
    print("Spojení uzavřeno.")
