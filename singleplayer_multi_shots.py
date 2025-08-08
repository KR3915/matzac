from logic import *
import random
import time

hrac1_X = 5
hrac1_Y = 9
enemak_X = 5
strela1_Y = 9
strela1_X = 5

# Player movement cooldown
player_move_cooldown = 0
player_move_delay = 3  # frames between moves

# Multiple shots system
active_shots = []  # List of active shots
max_shots = 3  # Maximum number of shots on screen
shot_cooldown = 0
shot_delay = 10  # frames between shots

# Buff system variables - redesigned
buff_X = -1
buff_Y = -1
buff_type = None
buff_active = False
buff_timer = 0
buff_duration = 200  # frames - increased

# Enemy types
enemy_type = "normal"  # "normal", "yellow", "blue"
enemy_health = 1

# Clone system
clone_X = -1
clone_Y = -1
clone_active = False
clone_timer = 0
clone_duration = 300  # frames - increased

# Slow enemy system
enemy_slow_timer = 0
enemy_slow_duration = 250  # frames - increased
enemy_slow_active = False

# Rapid fire system
rapid_fire_active = False
rapid_fire_timer = 0
rapid_fire_duration = 150  # frames

# Performance optimization variables
frame_counter = 0
enemy_move_counter = 0
enemy_shot_counter = 0
yellow_spawn_counter = 0

# Initialize display
display.clear()
display.set_pixel(hrac1_X, hrac1_Y, "green")
display.set_pixel(enemak_X, 0, "orange")

class Shot:
    def __init__(self, x, y, owner="player"):
        self.x = x
        self.y = y
        self.owner = owner
        self.active = True

def spawn_yellow_enemy():
    global enemak_X, enemy_type, enemy_health
    enemak_X = random.randint(0, 9)
    enemy_type = "yellow"
    enemy_health = 1
    display.set_pixel(enemak_X, 0, "yellow")

def activate_buff():
    global buff_active, buff_type, buff_timer, clone_active, clone_timer, clone_X, clone_Y
    global enemy_slow_active, enemy_slow_timer, rapid_fire_active, rapid_fire_timer
    
    if buff_type == "big_shot":
        buff_active = True
        buff_timer = buff_duration
        print("Big shot activated!")
        
    elif buff_type == "clone":
        clone_active = True
        clone_timer = clone_duration
        clone_X = hrac1_X + 1  # Position clone next to player
        if clone_X > 9:
            clone_X = hrac1_X - 1  # If at edge, put clone on other side
        clone_Y = hrac1_Y
        print("Clone activated!")
        
    elif buff_type == "slow_enemy":
        enemy_slow_active = True
        enemy_slow_timer = enemy_slow_duration
        print("Enemy slow activated!")
        
    elif buff_type == "rapid_fire":
        rapid_fire_active = True
        rapid_fire_timer = rapid_fire_duration
        print("Rapid fire activated!")
    
    # Reset buff pickup
    buff_X = -1
    buff_Y = -1
    buff_type = None

def update_buffs():
    global buff_timer, buff_active, clone_timer, clone_active, enemy_slow_timer, enemy_slow_active
    global rapid_fire_active, rapid_fire_timer
    
    # Update big shot buff
    if buff_active:
        buff_timer -= 1
        if buff_timer <= 0:
            buff_active = False
    
    # Update clone buff
    if clone_active:
        clone_timer -= 1
        if clone_timer <= 0:
            clone_active = False
            display.set_pixel(clone_X, clone_Y, "black")
            clone_X = -1
            clone_Y = -1
    
    # Update enemy slow buff
    if enemy_slow_active:
        enemy_slow_timer -= 1
        if enemy_slow_timer <= 0:
            enemy_slow_active = False
            
    # Update rapid fire buff
    if rapid_fire_active:
        rapid_fire_timer -= 1
        if rapid_fire_timer <= 0:
            rapid_fire_active = False

def update_shots():
    global active_shots
    
    # Update all active shots
    shots_to_remove = []
    for shot in active_shots:
        if shot.owner == "player":
            # Move player shot up
            shot.y -= 1
            if shot.y < 0:
                shots_to_remove.append(shot)
            else:
                display.set_pixel(shot.x, shot.y, "red")
                # Check for enemy hits
                if shot.x == enemak_X and shot.y == 0:
                    hit_enemy()
                    shots_to_remove.append(shot)
        elif shot.owner == "clone":
            # Move clone shot up
            shot.y -= 1
            if shot.y < 0:
                shots_to_remove.append(shot)
            else:
                display.set_pixel(shot.x, shot.y, "cyan")
                # Check for enemy hits
                if shot.x == enemak_X and shot.y == 0:
                    hit_enemy()
                    shots_to_remove.append(shot)
    
    # Remove inactive shots
    for shot in shots_to_remove:
        if shot in active_shots:
            active_shots.remove(shot)

def create_shot(x, y, owner="player"):
    global active_shots, max_shots
    
    if len(active_shots) < max_shots:
        new_shot = Shot(x, y, owner)
        active_shots.append(new_shot)
        return True
    return False

def big_shot():
    global strela1_X, strela1_Y
    strela1_X = hrac1_X
    strela1_Y = hrac1_Y
    
    # Create 3x3 shot pattern
    shot_positions = [
        (strela1_X, strela1_Y),
        (strela1_X-1, strela1_Y) if strela1_X > 0 else None,
        (strela1_X+1, strela1_Y) if strela1_X < 9 else None,
        (strela1_X, strela1_Y-1) if strela1_Y > 0 else None,
        (strela1_X-1, strela1_Y-1) if strela1_X > 0 and strela1_Y > 0 else None,
        (strela1_X+1, strela1_Y-1) if strela1_X < 9 and strela1_Y > 0 else None,
        (strela1_X, strela1_Y-2) if strela1_Y > 1 else None,
        (strela1_X-1, strela1_Y-2) if strela1_X > 0 and strela1_Y > 1 else None,
        (strela1_X+1, strela1_Y-2) if strela1_X < 9 and strela1_Y > 1 else None
    ]
    
    # Filter out None positions
    valid_positions = [pos for pos in shot_positions if pos is not None]
    
    for pos_x, pos_y in valid_positions:
        display.set_pixel(pos_x, pos_y, "red")
    
    for strela1_Y in range(9, -1, -1):
        # Clear previous positions
        for pos_x, pos_y in valid_positions:
            if 0 <= pos_x <= 9 and 0 <= pos_y <= 9:
                display.set_pixel(pos_x, pos_y, "black")
        
        # Update positions
        new_positions = []
        for pos_x, pos_y in valid_positions:
            new_y = pos_y - 1
            if new_y >= 0:
                new_positions.append((pos_x, new_y))
                display.set_pixel(pos_x, new_y, "red")
        
        valid_positions = new_positions
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        
        # Check for enemy hits
        for pos_x, pos_y in valid_positions:
            if pos_x == enemak_X and pos_y == 0:
                hit_enemy()
                return
        
        time.sleep_ms(50)  # Reduced from 100ms for smoother gameplay
        
        # Player movement during shot
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()
        
        pohyb_enemaka()

def hit_enemy():
    global enemy_type, enemy_health, buff_X, buff_Y, buff_type, enemak_X
    
    if enemy_type == "yellow":
        enemy_health -= 1
        if enemy_health <= 0:
            # Enemy defeated, spawn buff at player's level
            buff_X = enemak_X
            buff_Y = 8  # Spawn buff at player's level (Y=8) instead of top (Y=0)
            buff_type = random.choice(["big_shot", "clone", "slow_enemy", "rapid_fire"])
            display.set_pixel(enemak_X, 0, "lightblue")
            print(f"Buff dropped: {buff_type}")
            # Reset to normal enemy
            enemy_type = "normal"
            enemy_health = 1
        else:
            # Enemy hit but not defeated
            display.set_pixel(enemak_X, 0, "yellow")
    else:
        # Normal enemy defeated
        prohra()

def strela1_do_leva():
    global strela1_X
    display.set_pixel(strela1_X, strela1_Y, "black")
    strela1_X = strela1_X - 1
    display.set_pixel(strela1_X, strela1_Y, "red")

def strela1_do_prava():
    global strela1_X
    display.set_pixel(strela1_X, strela1_Y, "black")
    strela1_X = strela1_X + 1
    display.set_pixel(strela1_X, strela1_Y, "red")

def hrac1_do_leva():
    global hrac1_X, player_move_cooldown
    if player_move_cooldown <= 0:
        display.set_pixel(hrac1_X, hrac1_Y, "black")
        hrac1_X = hrac1_X - 1
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        player_move_cooldown = player_move_delay

def hrac1_do_prava():
    global hrac1_X, player_move_cooldown
    if player_move_cooldown <= 0:
        display.set_pixel(hrac1_X, hrac1_Y, "black")
        hrac1_X = hrac1_X + 1
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        player_move_cooldown = player_move_delay

def hrac1_vystrel():
    global shot_cooldown, rapid_fire_active
    
    # Check if we can shoot (cooldown system)
    if shot_cooldown <= 0:
        # Create player shot
        if create_shot(hrac1_X, hrac1_Y, "player"):
            shot_cooldown = shot_delay
            # If rapid fire is active, reduce cooldown
            if rapid_fire_active:
                shot_cooldown = shot_delay // 3
        
        # Create clone shot if active
        if clone_active:
            create_shot(clone_X, clone_Y, "clone")



def flashbang() :
    c = 0
    d = 0
    for d in range(10):
        for c in range(10):
            display.set_pixel(c, d, "white")
    time.sleep_ms(1000)
    display.clear()

def laser():
    global strela1_X, strela1_Y
    strela1_X = hrac1_X
    strela1_Y = hrac1_Y + 1
    cesta_laseru = []
    zacatek_laseru = strela1_X
    
    # First phase - record path
    for strela1_Y in range(8, -1, -1):
        display.set_pixel(strela1_X, strela1_Y, "red")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(150)  # Increased for better control

        # Shot movement
        if buttons_b.left and strela1_X > 0:
            strela1_do_leva()
            cesta_laseru.append(-1)
        elif buttons_b.right and strela1_X < 9:
            strela1_do_prava()
            cesta_laseru.append(1)
        else:
            cesta_laseru.append(0)

        # Player movement (slower for better control)
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        # Enemy movement (less frequent)
        if strela1_Y % 3 == 0:
            pohyb_enemaka()
    
    print(cesta_laseru)

    # Second phase - follow path back
    for strela1_Y in range(0, 9, 1):
        zacatek_laseru = zacatek_laseru + cesta_laseru[strela1_Y]
        display.set_pixel(zacatek_laseru, 8-strela1_Y, "black")
        display.set_pixel(hrac1_X, hrac1_Y, "green")

        # Check for enemy hit
        if enemak_X == strela1_X:
            # Explosion effect
            for i in range(9):
                d = i + 1
                if strela1_X - d > -1:
                    display.set_pixel(strela1_X - d + 1, i, "black")
                    display.set_pixel(strela1_X - d, i, "red")
                if strela1_X + d < 10:
                    display.set_pixel(strela1_X + d - 1, i, "black")
                    display.set_pixel(strela1_X + d, i, "red")
                time.sleep_ms(100)  # Reduced from 200ms
            display.set_pixel(0, 8, "black")
            display.set_pixel(9, 8, "black")
            prohra()
            strela1_Y = 5
            return()

        time.sleep_ms(100)  # Increased for better control

        # Player movement (slower for better control)
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        # Enemy movement (less frequent)
        if strela1_Y % 3 == 0:
            pohyb_enemaka()

    # Clean up laser path
    if strela1_X == 9:
        display.set_pixel(zacatek_laseru, 0, "black")
        display.set_pixel(zacatek_laseru - 1, 0, "black")
    elif strela1_X == 0:
        display.set_pixel(zacatek_laseru + 1, 0, "black")
        display.set_pixel(zacatek_laseru, 0, "black")
    else:
        display.set_pixel(zacatek_laseru + 1, 0, "black")
        display.set_pixel(zacatek_laseru, 0, "black")
        display.set_pixel(zacatek_laseru - 1, 0, "black")
        

def strileni_soucasne():
    global enemak_strela_Y, enemak_strela_X, strela1_Y, strela1_X
    
    # Clear initial positions
    display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
    display.set_pixel(strela1_X, strela1_Y, "black")
    
    for i in range(9):
        # Move player shot up
        if strela1_Y > 0:
            strela1_Y -= 1
            display.set_pixel(strela1_X, strela1_Y, "red") 
            enemak_smrt()   

        # Move enemy shot down
        if enemak_strela_Y < 9:
            enemak_strela_Y += 1
            display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
            hrac1_smrt()
        
        # Update player and enemy display
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        if enemy_type == "yellow":
            display.set_pixel(enemak_X, 0, "yellow")
        else:
            display.set_pixel(enemak_X, 0, "orange")

        # Player movement
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        # Shot movement
        if buttons_b.left and strela1_X > 0:
            strela1_do_leva()
        if buttons_b.right and strela1_X < 9:
            strela1_do_prava()

        # Enemy movement (less frequent)
        if i % 2 == 0:
            pohyb_enemaka()

        time.sleep_ms(50)  # Reduced from 100ms
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
        display.set_pixel(strela1_X, strela1_Y, "black")
    
    time.sleep_ms(50)  # Reduced from 100ms


def strileni_enemaka():
    global enemak_strela_Y, enemak_strela_X, strela1_Y, strela1_X
    
    enemak_strela_X = enemak_X
    enemak_strela_Y = 0  # Start from top
    
    for enemak_strela_Y in range(10):
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
        
        # Update enemy display with correct color
        if enemy_type == "yellow":
            display.set_pixel(enemak_X, 0, "yellow")
        else:
            display.set_pixel(enemak_X, 0, "orange")
            
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(50)  # Reduced from 100ms

        # Player movement
        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava() 

        # Enemy movement (less frequent)
        if enemak_strela_Y % 2 == 0:
            pohyb_enemaka()
            
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")

        # Check for player counter-shot
        if buttons_a.enter:
            strela1_X = hrac1_X
            strela1_Y = 9
            strileni_soucasne()
            enemak_strela_Y = 0
            strela1_Y = 1
            return ()
            
        hrac1_smrt()

    enemak_strela_Y = 0



       
def hrac1_smrt() :
    global enemak_strela_X
    global enemak_strela_Y
    global hrac1_X
    if enemak_strela_X == hrac1_X and enemak_strela_Y == 9 :
        c = 9
        d = 0
        for i in range(9):
            d += 1
            if enemak_strela_X - d > -1 :
                display.set_pixel(enemak_strela_X - d + 1, c, "black")
                display.set_pixel(enemak_strela_X - d, c, "red")
            if enemak_strela_X + d < 10 :
                display.set_pixel(enemak_strela_X + d - 1, c, "black")
                display.set_pixel(enemak_strela_X + d, c, "red")
            i = i + 1
            time.sleep_ms(200)
        display.set_pixel(0, c, "black")
        display.set_pixel(9, c, "black")
        prohra()

def pohyb_enemaka():
    global enemak_X, enemy_slow_active
    
    # Slow enemy movement if buff is active
    if enemy_slow_active:
        if random.randint(1, 3) != 1:  # 1/3 chance to move
            return
    
    # Simplified movement logic
    g = [-1, 0, 0, 0, 0, 0, 0, 1]
    e = g[random.randint(0, 7)]
    
    # Check boundaries
    if (enemak_X == 0 and e == -1) or (enemak_X == 9 and e == 1):
        return  # Don't move if at boundary
    
    # Move enemy
    display.set_pixel(enemak_X, 0, "black")
    enemak_X = enemak_X + e
    
    # Set correct color
    if enemy_type == "yellow":
        display.set_pixel(enemak_X, 0, "yellow")
    else:
        display.set_pixel(enemak_X, 0, "orange")

def enemak_smrt() :
    global strela1_Y
    global strela1_X
    global enemak_X
    if strela1_X == enemak_X and strela1_Y == 0 :
        hit_enemy()



def prohra() :
    while True :
        if buttons_a.enter :
            display.clear()
            return ()

while True:
    # Update frame counter
    frame_counter += 1
    
    # Update cooldowns
    if player_move_cooldown > 0:
        player_move_cooldown -= 1
    if shot_cooldown > 0:
        shot_cooldown -= 1
    
    # Update buffs
    update_buffs()
    
    # Update shots
    update_shots()
    
    # Display buff if available
    if buff_X != -1 and buff_Y != -1:
        if buff_type == "big_shot":
            display.set_pixel(buff_X, buff_Y, "purple")
        elif buff_type == "clone":
            display.set_pixel(buff_X, buff_Y, "cyan")
        elif buff_type == "slow_enemy":
            display.set_pixel(buff_X, buff_Y, "blue")
        elif buff_type == "rapid_fire":
            display.set_pixel(buff_X, buff_Y, "yellow")
    
    # Display clone if active
    if clone_active:
        display.set_pixel(clone_X, clone_Y, "cyan")
    
    # Player movement (with cooldown)
    if buttons_a.left and hrac1_X > 0:
        hrac1_do_leva()
        # Move clone with player
        if clone_active:
            display.set_pixel(clone_X, clone_Y, "black")
            clone_X = hrac1_X + 1
            if clone_X > 9:
                clone_X = hrac1_X - 1
            display.set_pixel(clone_X, clone_Y, "cyan")
            
    if buttons_a.right and hrac1_X < 9:
        hrac1_do_prava()
        # Move clone with player
        if clone_active:
            display.set_pixel(clone_X, clone_Y, "black")
            clone_X = hrac1_X + 1
            if clone_X > 9:
                clone_X = hrac1_X - 1
            display.set_pixel(clone_X, clone_Y, "cyan")

    # Check for buff pickup (after movement)
    if buff_X != -1 and buff_Y != -1:
        if hrac1_X == buff_X and hrac1_Y == buff_Y:
            activate_buff()

    # Player shooting
    if buttons_a.enter:
        if buff_active and buff_type == "big_shot":
            big_shot()
        else:
            hrac1_vystrel()
    
    # Special abilities
    if buttons_b.enter:
        flashbang()
    if buttons_b.up:
        laser()
    
    # Activate buff with down button
    if buttons_b.down and buff_X != -1 and buff_Y != -1:
        activate_buff()

    # Enemy movement (every 3 frames for better performance)
    if frame_counter % 3 == 0:
        pohyb_enemaka()

    # Enemy shooting (reduced frequency)
    if frame_counter % 10 == 0 and random.randint(1, 15) == 1:
        strileni_enemaka()
    
    # Spawn yellow enemy (reduced frequency)
    if frame_counter % 20 == 0 and random.randint(1, 25) == 1 and enemy_type == "normal":
        spawn_yellow_enemy()
    
    # Small delay for smooth gameplay
    time.sleep_ms(20)
