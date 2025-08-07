import time
import random

# --- Herní konstanty pro Logic v2.0 (10x10) ---
DISPLAY_WIDTH = 10
DISPLAY_HEIGHT = 10
PLAYER_START_X = 5
PLAYER_START_Y = 9  # Hráč hraje úplně dole (řádek 9)
MAX_SHOTS = 6  # Optimální počet střel pro 10x10

# --- Herní stav ---
class SinglePlayerGameState:
    def __init__(self):
        # Hráč (dole)
        self.player_x = PLAYER_START_X
        self.player_y = PLAYER_START_Y
        self.player_alive = True
        self.player_shots = []  # Seznam střel hráče
        
        # Nepřátelé
        self.enemies = []
        self.init_enemies()
        
        # Skóre
        self.score = 0
        
        # Herní stav
        self.game_over = False
        self.level = 1

    def init_enemies(self):
        self.enemies = []
        # Vytvoříme nepřátele v horní části obrazovky (řádky 0-3)
        for row in range(2):  # 2 řádky nepřátel
            for col in range(8):  # 8 nepřátel v řádku
                if col < DISPLAY_WIDTH - 1:  # Necháme místo na okrajích
                    self.enemies.append({
                        'x': col + 1,
                        'y': row + 1,
                        'alive': True,
                        'type': 'normal'
                    })

    def move_player(self, direction):
        if not self.player_alive:
            return
        if direction == 'left' and self.player_x > 0:
            self.player_x -= 1
        elif direction == 'right' and self.player_x < DISPLAY_WIDTH - 1:
            self.player_x += 1

    def player_shoot(self):
        if not self.player_alive or len(self.player_shots) >= MAX_SHOTS:
            return
        # Přidáme novou střelu
        self.player_shots.append({
            'x': self.player_x,
            'y': self.player_y - 1,
            'active': True
        })

    def update_shots(self):
        # Pohyb střel hráče (nahoru)
        shots_to_remove = []
        for i, shot in enumerate(self.player_shots):
            if shot['active']:
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
                            self.score += 10
                            break
        
        # Odstraníme střely, které zasáhly nebo opustily obrazovku
        for i in reversed(shots_to_remove):
            if i < len(self.player_shots):
                self.player_shots.pop(i)

    def move_enemies(self):
        # Chytřejší pohyb nepřátel
        for enemy in self.enemies:
            if enemy['alive']:
                # Náhodný pohyb s větší pravděpodobností zůstat na místě
                if random.randint(0, 25) == 0:  # Pomalejší pohyb
                    direction = random.choice([-1, 0, 1])
                    new_x = enemy['x'] + direction
                    if 0 <= new_x < DISPLAY_WIDTH:
                        enemy['x'] = new_x

    def check_game_over(self):
        # Kontrola, zda jsou všichni nepřátelé mrtví
        alive_enemies = sum(1 for enemy in self.enemies if enemy['alive'])
        if alive_enemies == 0:
            self.game_over = True

def render_display(game_state):
    """Vykreslí herní stav na displej 10x10"""
    # Vyčistíme displej
    display.clear()
    
    # Vykreslíme hráče (zelený)
    if game_state.player_alive:
        display.set_pixel(game_state.player_x, game_state.player_y, "green")
    
    # Vykreslíme střely hráče (žluté)
    for shot in game_state.player_shots:
        if shot['active'] and 0 <= shot['y'] < DISPLAY_HEIGHT:
            display.set_pixel(shot['x'], shot['y'], "yellow")
    
    # Vykreslíme nepřátele (oranžoví)
    for enemy in game_state.enemies:
        if enemy['alive']:
            display.set_pixel(enemy['x'], enemy['y'], "orange")

def show_game_over():
    """Zobrazí konec hry na 10x10 displeji"""
    display.clear()
    
    # Zelená obrazovka = výhra
    for x in range(DISPLAY_WIDTH):
        for y in range(DISPLAY_HEIGHT):
            display.set_pixel(x, y, "green")
    time.sleep(1.5)
    
    # Animované skóre
    for _ in range(3):
        display.clear()
        time.sleep(0.3)
        
        # Zobrazíme skóre jako světlé pixely
        score_display = min(game_state.score // 10, DISPLAY_WIDTH * DISPLAY_HEIGHT)
        pixels_shown = 0
        
        for x in range(DISPLAY_WIDTH):
            for y in range(DISPLAY_HEIGHT):
                if pixels_shown < score_display:
                    display.set_pixel(x, y, "white")
                    pixels_shown += 1
        
        time.sleep(0.7)

def show_start_screen():
    """Zobrazí úvodní obrazovku"""
    display.clear()
    
    # Animace - postupně se rozsvítí displej
    for y in range(DISPLAY_HEIGHT):
        for x in range(DISPLAY_WIDTH):
            display.set_pixel(x, y, "blue")
            time.sleep(0.05)
    
    time.sleep(1)
    display.clear()

# --- Hlavní smyčka ---
print("=== Space Invaders pro Logic v2.0 ===")
print("Ovládání: A+levo/pravo = pohyb, A+Enter = střelba")
print("Můžete střílet až", MAX_SHOTS, "střel najednou!")
print("Cíl: Zničte všechny nepřátele!")

# Zobrazíme úvodní obrazovku
show_start_screen()

# Inicializace hry
game_state = SinglePlayerGameState()

try:
    while True:
        # --- Herní logika ---
        # Ovládání hráče
        if buttons_a.left:
            game_state.move_player('left')
        if buttons_a.right:
            game_state.move_player('right')
        if buttons_a.enter:
            game_state.player_shoot()
        
        # Aktualizace střel
        game_state.update_shots()
        
        # Pohyb nepřátel
        game_state.move_enemies()
        
        # Kontrola konce hry
        game_state.check_game_over()
        
        # Vykreslení
        render_display(game_state)
        
        # Kontrola konce hry
        if game_state.game_over:
            print(f"🎉 VÝHRA! Skóre: {game_state.score}")
            show_game_over()
            
            # Čekání na restart
            print("Stiskněte A+Enter pro novou hru")
            while True:
                if buttons_a.enter:
                    # Restart hry
                    game_state = SinglePlayerGameState()
                    print("🚀 Nová hra!")
                    break
                time.sleep(0.1)
        
        time.sleep(0.08)  # ~12 FPS pro plynulejší hru

except KeyboardInterrupt:
    print("Hra ukončena")
except Exception as e:
    print(f"Chyba: {e}")
