from logic import *
import random
import time

# Herní proměnné
hrac1_X = 5
hrac1_Y = 9
enemak_X = 5
# Změna z jednoho střelu na více střelů
strela_list = []  # List of active shots: [(x, y), (x, y), ...]

def strela_do_leva(strela_index):
    global strela_list
    if strela_index < len(strela_list):
        time.sleep_ms(100)
        display.set_pixel(strela_list[strela_index][0], strela_list[strela_index][1], "black")
        strela_list[strela_index][0] = strela_list[strela_index][0] - 1
        display.set_pixel(strela_list[strela_index][0], strela_list[strela_index][1], "red")
    return

def strela_do_prava(strela_index):
    global strela_list
    if strela_index < len(strela_list):
        time.sleep_ms(100)
        display.set_pixel(strela_list[strela_index][0], strela_list[strela_index][1], "black")
        strela_list[strela_index][0] = strela_list[strela_index][0] + 1
        display.set_pixel(strela_list[strela_index][0], strela_list[strela_index][1], "red")
    return

def hrac1_do_leva():
    global hrac1_X
    time.sleep_ms(100)
    display.set_pixel(hrac1_X, hrac1_Y, "black")
    hrac1_X = hrac1_X - 1
    display.set_pixel(hrac1_X, hrac1_Y, "green")
    return

def hrac1_do_prava():
    global hrac1_X
    time.sleep_ms(100)
    display.set_pixel(hrac1_X, hrac1_Y, "black")
    hrac1_X = hrac1_X + 1
    display.set_pixel(hrac1_X, hrac1_Y, "green")
    return

def hrac1_vystrel():
    global strela_list
    # Add new shot to the list
    strela_list.append([hrac1_X, hrac1_Y])
    
    # Process all active shots
    for i, shot in enumerate(strela_list[:]):  # Create copy to iterate
        if shot[1] > 0:  # If shot hasn't reached the top
            display.set_pixel(shot[0], shot[1], "red")
            display.set_pixel(hrac1_X, hrac1_Y, "green")
            time.sleep_ms(50)  # Faster movement for multiple shots

            if buttons_a.left and hrac1_X > 0:
                hrac1_do_leva()

            if buttons_a.right and hrac1_X < 9:
                hrac1_do_prava()

            # Check for enemy shooting during player shot
            p = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            if p[random.randint(0, 10)] == 1:
                global enemak_strela_X
                global enemak_X
                global enemak_strela_Y
                enemak_strela_X = enemak_X
                enemak_strela_Y = 1
                strileni_soucasne()
                enemak_strela_Y = 0
                shot[1] = 1
                return ()
            
            # Control individual shots with buttons_b
            if buttons_b.left and shot[0] > 0:
                strela_do_leva(i)

            if buttons_b.right and shot[0] < 9:
                strela_do_prava(i)

            pohyb_enemaka()
            enemak_smrt()

            display.set_pixel(shot[0], shot[1], "black")
            # Move shot up
            shot[1] -= 1
        else:
            # Remove shot that reached the top
            strela_list.remove(shot)

def flashbang():
    c = 0
    d = 0
    for d in range(10):
        for c in range(10):
            display.set_pixel(c, d, "white")
    time.sleep_ms(1000)
    display.clear()

def laser():
    global strela_list
    # Add new laser shot to the list
    strela_list.append([hrac1_X, hrac1_Y])
    
    # Process all active shots including the new laser
    for i, shot in enumerate(strela_list[:]):  # Create copy to iterate
        if shot[1] > 0:  # If shot hasn't reached the top
            display.set_pixel(shot[0], shot[1], "red")
            display.set_pixel(hrac1_X, hrac1_Y, "green")
            time.sleep_ms(50)  # Faster movement for multiple shots

            if buttons_a.left and hrac1_X > 0:
                hrac1_do_leva()

            if buttons_a.right and hrac1_X < 9:
                hrac1_do_prava()

            pohyb_enemaka()
            display.set_pixel(shot[0], shot[1], "black")
            # Move shot up
            shot[1] -= 1
        else:
            # Remove shot that reached the top
            strela_list.remove(shot)
    
    # Laser effect - check for enemy hit
    for shot in strela_list[:]:
        if shot[0] == enemak_X and shot[1] <= 0:
            # Laser hit enemy
            d = 0
            c = 0
            for i in range(9):
                d += 1
                if shot[0] - d > -1:
                    display.set_pixel(shot[0] - d + 1, c, "black")
                    display.set_pixel(shot[0] - d, c, "red")
                if shot[0] + d < 10:
                    display.set_pixel(shot[0] + d - 1, c, "black")
                    display.set_pixel(shot[0] + d, c, "red")
                i = i + 1
                time.sleep_ms(200)
            display.set_pixel(0, c, "black")
            display.set_pixel(9, c, "black")
            prohra()
            return()

def strileni_soucasne():
    global enemak_strela_Y
    global enemak_strela_X
    global strela_list
    display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
    
    # Clear all player shots
    for shot in strela_list:
        display.set_pixel(shot[0], shot[1], "black")
    
    i = 0
    c = 0
    d = 0
    for i in range(9):
        # Move all player shots up
        for shot in strela_list[:]:
            if shot[1] > 0:
                shot[1] -= 1
                display.set_pixel(shot[0], shot[1], "red") 
                enemak_smrt()   

        if enemak_strela_Y < 9:
            enemak_strela_Y += 1
            display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
            hrac1_smrt()
        
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        display.set_pixel(enemak_X, 0, "orange")

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()

        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava()

        pohyb_enemaka()

        time.sleep_ms(100)
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")
        # Clear all player shots
        for shot in strela_list:
            display.set_pixel(shot[0], shot[1], "black")
    time.sleep_ms(100)
    return()

def strileni_enemaka():
    global enemak_strela_Y
    global enemak_strela_X
    enemak_strela_X = enemak_X
    enemak_strela_Y = 9
    global strela_list
    for enemak_strela_Y in range(10):
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "red")
        display.set_pixel(enemak_X, 0, "orange")
        display.set_pixel(hrac1_X, hrac1_Y, "green")
        time.sleep_ms(100)

        if buttons_a.left and hrac1_X > 0:
            hrac1_do_leva()
        if buttons_a.right and hrac1_X < 9:
            hrac1_do_prava() 

        pohyb_enemaka()
        display.set_pixel(enemak_strela_X, enemak_strela_Y, "black")

        if buttons_a.enter:
            # Add new shot when player shoots during enemy attack
            strela_list.append([hrac1_X, hrac1_Y])
            strileni_soucasne()
            enemak_strela_Y = 0
            return ()
        hrac1_smrt()

    enemak_strela_Y = 0

def hrac1_smrt():
    global enemak_strela_X
    global enemak_strela_Y
    global hrac1_X
    if enemak_strela_X == hrac1_X and enemak_strela_Y == 9:
        c = 9
        d = 0
        for i in range(9):
            d += 1
            if enemak_strela_X - d > -1:
                display.set_pixel(enemak_strela_X - d + 1, c, "black")
                display.set_pixel(enemak_strela_X - d, c, "red")
            if enemak_strela_X + d < 10:
                display.set_pixel(enemak_strela_X + d - 1, c, "black")
                display.set_pixel(enemak_strela_X + d, c, "red")
            i = i + 1
            time.sleep_ms(200)
        display.set_pixel(0, c, "black")
        display.set_pixel(9, c, "black")
        prohra()

def pohyb_enemaka():
    global enemak_X
    g = [-1, 0, 0, 0, 0, 0, 0, 1]
    e = g[random.randint(0,7)]
    if enemak_X == 0 and e == -1:
        display.set_pixel(enemak_X, 0, "orange")
    elif enemak_X == 9 and e == 1:
        display.set_pixel(enemak_X, 0, "orange")
    else:
        display.set_pixel(enemak_X, 0, "black")
        enemak_X = enemak_X + e
        display.set_pixel(enemak_X, 0, "orange")
        time.sleep_ms(100)

def enemak_smrt():
    global strela_list
    global enemak_X
    # Check all shots for enemy hit
    for shot in strela_list[:]:
        if shot[0] == enemak_X and shot[1] == 0:
            d = 0
            c = 0
            for i in range(9):
                d += 1
                if shot[0] - d > -1:
                    display.set_pixel(shot[0] - d + 1, c, "black")
                    display.set_pixel(shot[0] - d, c, "red")
                if shot[0] + d < 10:
                    display.set_pixel(shot[0] + d - 1, c, "black")
                    display.set_pixel(shot[0] + d, c, "red")
                i = i + 1
                time.sleep_ms(200)
            display.set_pixel(0, c, "black")
            display.set_pixel(9, c, "black")
            # Remove the shot that hit
            strela_list.remove(shot)
            prohra()

def prohra():
    while True:
        if buttons_a.enter:
            display.clear()
            return ()

# Hlavní smyčka hry
while True:
    if buttons_a.left and hrac1_X > 0:
        hrac1_do_leva()

    if buttons_a.right and hrac1_X < 9:
       hrac1_do_prava()     

    if buttons_a.enter:
        hrac1_vystrel()
    
    if buttons_b.enter:
        flashbang()

    pohyb_enemaka()

    p = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    if p[random.randint(0, 10)] == 1:
        strileni_enemaka()
    
    if buttons_b.up:
        laser()
