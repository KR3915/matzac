from singleplayer_multi_shots import SinglePlayerGame
from host import MultiplayerHost
from client import MultiplayerClient
import time

def show_menu(display, buttons_a, buttons_b):
    """Show game mode selection menu"""
    display.clear()
    
    # Draw menu options
    menu_pixels = [
        # "SINGLE"
        (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
        (1, 3), (7, 3),
        (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
        # "MULTI"
        (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
        (1, 7), (7, 7),
        (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
    ]
    
    for x, y in menu_pixels:
        display.set_pixel(x, y, "white")
        
    # Selection indicator
    display.set_pixel(0, 3, "green")  # Single player selected by default
    
    selection = 0  # 0 = single player, 1 = multiplayer
    
    while True:
        if buttons_a.up and selection > 0:
            selection = 0
            display.set_pixel(0, 3, "green")
            display.set_pixel(0, 7, "black")
        elif buttons_a.down and selection < 1:
            selection = 1
            display.set_pixel(0, 3, "black")
            display.set_pixel(0, 7, "green")
        elif buttons_a.enter:
            return selection
            
        time.sleep_ms(100)

def show_multiplayer_menu(display, buttons_a, buttons_b):
    """Show multiplayer mode selection menu"""
    display.clear()
    
    # Draw menu options
    menu_pixels = [
        # "HOST"
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
        (2, 3), (6, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
        # "CLIENT"
        (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
        (1, 7), (7, 7),
        (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
    ]
    
    for x, y in menu_pixels:
        display.set_pixel(x, y, "white")
        
    # Selection indicator
    display.set_pixel(0, 3, "green")  # Host selected by default
    
    selection = 0  # 0 = host, 1 = client
    
    while True:
        if buttons_a.up and selection > 0:
            selection = 0
            display.set_pixel(0, 3, "green")
            display.set_pixel(0, 7, "black")
        elif buttons_a.down and selection < 1:
            selection = 1
            display.set_pixel(0, 3, "black")
            display.set_pixel(0, 7, "green")
        elif buttons_a.enter:
            return selection
            
        time.sleep_ms(100)

def main():
    """Main game launcher"""
    # These should be imported from your hardware interface
    # display = your_display_object
    # buttons_a = your_buttons_a_object
    # buttons_b = your_buttons_b_object
    
    print("Space Invaders - Optimized Version")
    print("Shot limit: 5 per player, unlimited for enemies")
    
    # Show main menu
    game_mode = show_menu(display, buttons_a, buttons_b)
    
    if game_mode == 0:
        # Single player mode
        print("Starting single player game...")
        game = SinglePlayerGame(display, buttons_a, buttons_b)
        game.game_loop()
    else:
        # Multiplayer mode
        print("Starting multiplayer game...")
        multi_mode = show_multiplayer_menu(display, buttons_a, buttons_b)
        
        if multi_mode == 0:
            # Host mode
            print("Starting as host...")
            host = MultiplayerHost(display, buttons_a, buttons_b)
            host.run_game()
        else:
            # Client mode
            print("Starting as client...")
            client = MultiplayerClient(display, buttons_a, buttons_b)
            client.run_game()

if __name__ == "__main__":
    # Uncomment and modify these lines to match your hardware setup
    # from your_hardware_module import display, buttons_a, buttons_b
    # main()
    
    print("Space Invaders - Optimized Version")
    print("Please configure your hardware interface and uncomment the main() call")
    print("Features:")
    print("- Shot limit: 5 per player")
    print("- Unlimited enemy shots")
    print("- Shot replenishment over time")
    print("- Multiple active shots support")
    print("- Optimized collision detection")
    print("- Single player and multiplayer modes")
