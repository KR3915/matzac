import time
import random

# --- Herní konstanty ---
DISPLAY_WIDTH = 10
DISPLAY_HEIGHT = 20
PLAYER_START_X = 5
PLAYER_START_Y = 18  # Hráč hraje dole
MAX_SHOTS = 10  # Maximální počet střel najednou

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
            'y': self.player_y - 1
        })

    def update_shots(self):
        # Pohyb střel hráče (nahoru)
        shots_to_remove = []
        for i, shot in enumerate(self.player_shots):
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
        # Jednoduchý pohyb nepřátel
        for enemy in self.enemies:
            if enemy['alive']:
                # Náhodný pohyb
                if random.randint(0, 15) == 0:  # Pomalejší pohyb
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
    """Vykreslí herní stav na displej"""
    # Vyčistíme displej
    display.clear()
    
    # Vykreslíme hráče (zelený)
    if game_state.player_alive:
        display.set_pixel(game_state.player_x, game_state.player_y, "green")
    
    # Vykreslíme střely hráče (žluté)
    for shot in game_state.player_shots:
        if 0 <= shot['y'] < DISPLAY_HEIGHT:
            display.set_pixel(shot['x'], shot['y'], "yellow")
    
    # Vykreslíme nepřátele (oranžoví)
    for enemy in game_state.enemies:
        if enemy['alive']:
            display.set_pixel(enemy['x'], enemy['y'], "orange")

def show_game_over():
    """Zobrazí konec hry"""
    display.clear()
    # Zelená obrazovka = výhra
    for x in range(DISPLAY_WIDTH):
        for y in range(DISPLAY_HEIGHT):
            display.set_pixel(x, y, "green")
    time.sleep(2)
    
    # Blikající skóre
    for _ in range(5):
        display.clear()
        time.sleep(0.5)
        # Zobrazíme skóre jako světlé pixely
        score_display = min(game_state.score // 10, DISPLAY_WIDTH * DISPLAY_HEIGHT)
        pixels_shown = 0
        for x in range(DISPLAY_WIDTH):
            for y in range(DISPLAY_HEIGHT):
                if pixels_shown < score_display:
                    display.set_pixel(x, y, "white")
                    pixels_shown += 1
        time.sleep(0.5)

# --- Hlavní smyčka ---
print("Singleplayer Space Invaders Test")
print("Ovládání: A+levo/pravo = pohyb, A+Enter = střelba")
print("Můžete střílet až", MAX_SHOTS, "střel najednou!")

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
            print(f"Game Over! Skóre: {game_state.score}")
            show_game_over()
            
            # Čekání na restart
            print("Stiskněte A+Enter pro restart")
            while True:
                if buttons_a.enter:
                    # Restart hry
                    game_state = SinglePlayerGameState()
                    print("Nová hra!")
                    break
                time.sleep(0.1)
        
        time.sleep(0.1)  # 10 FPS

except KeyboardInterrupt:
    print("Hra ukončena")
except Exception as e:
    print(f"Chyba: {e}")
