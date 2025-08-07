import network
import socket
import ujson
import time
from game_logic import GameState

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP-AP", password="protabulesa", authmode=network.AUTH_WPA2_PSK)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))
s.listen(1)

print(f"Server running! | IP: {ap.ifconfig()[0]}")

game = GameState()

while True:
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn.settimeout(5.0)
    print(f"Client connected from: {addr}")

    try:
        while True:
            # 1. Receive client action
            try:
                line = conn.readline()
                if not line:
                    print("Client disconnected gracefully.")
                    break
                client_msg = ujson.loads(line)
                client_action = client_msg.get('action')
            except Exception as e:
                print(f"Error receiving client action: {e}")
                client_action = None

            # 2. Handle local (host) input
            # Replace this with real input handling for your hardware
            host_action = input("Host action (left/right/shoot/none): ")
            if host_action == 'left':
                game.move_player('host', 'left')
            elif host_action == 'right':
                game.move_player('host', 'right')
            elif host_action == 'shoot':
                game.player_shoot('host')

            # 3. Apply client action
            if client_action == 'left':
                game.move_player('client', 'left')
            elif client_action == 'right':
                game.move_player('client', 'right')
            elif client_action == 'shoot':
                game.player_shoot('client')

            # 4. Update game state
            game.update_shots()
            game.move_enemy()
            # game.render()  # Implement for your display

            # 5. Send updated state to client
            state_to_send = ujson.dumps(game.to_dict()) + '\n'
            conn.sendall(state_to_send.encode('utf-8'))
            time.sleep(0.1)

    except OSError as e:
        print(f"Connection with {addr} lost: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed. Ready for next client.")