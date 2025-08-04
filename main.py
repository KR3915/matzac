from logic import *
import time

x1, y1 = 0, 9
x2, y2 = 9, 0

projectiles = []

player1_alive = True
player2_alive = True

player1_hit_time = None
player2_hit_time = None

while True:
    now = time.ticks_ms()

    # Obnova hráčů po 10 sekundách
    if not player1_alive and time.ticks_diff(now, player1_hit_time) >= 10000:
        player1_alive = True
        x1, y1 = 0, 9  # Reset pozice hráče 1

    if not player2_alive and time.ticks_diff(now, player2_hit_time) >= 10000:
        player2_alive = True
        x2, y2 = 9, 0  # Reset pozice hráče 2

    # Pohyb hráče 1
    if player1_alive:
        if buttons_a.left and x1 > 0:
            x1 -= 1
        if buttons_a.right and x1 < 9:
            x1 += 1
        if buttons_a.up and y1 > 0:
            y1 -= 1
        if buttons_a.down and y1 < 9:
            y1 += 1
        if buttons_a.enter:
            projectiles.append({'x': x1, 'y': y1 - 1, 'dy': -1, 'color': 'white'})

    # Pohyb hráče 2
    if player2_alive:
        if buttons_b.left and x2 > 0:
            x2 -= 1
        if buttons_b.right and x2 < 9:
            x2 += 1
        if buttons_b.up and y2 > 0:
            y2 -= 1
        if buttons_b.down and y2 < 9:
            y2 += 1
        if buttons_b.enter:
            projectiles.append({'x': x2, 'y': y2 + 1, 'dy': 1, 'color': 'red'})

    # Pohyb projektilů
    new_projectiles = []
    for p in projectiles:
        p['y'] += p['dy']
        if 0 <= p['y'] <= 9:
            # Detekce zásahu hráče
            if player2_alive and p['x'] == x2 and p['y'] == y2 and p['color'] == 'white':
                player2_alive = False
                player2_hit_time = now
                continue
            if player1_alive and p['x'] == x1 and p['y'] == y1 and p['color'] == 'red':
                player1_alive = False
                player1_hit_time = now
                continue
            new_projectiles.append(p)

    projectiles = new_projectiles

    # Zobrazení
    display.clear()
    if player1_alive:
        display.set_pixel(x1, y1, 'white')
    if player2_alive:
        display.set_pixel(x2, y2, 'red')
    for p in projectiles:
        display.set_pixel(p['x'], p['y'], p['color'])

    time.sleep_ms(150)
