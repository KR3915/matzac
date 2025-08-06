from logic import *
import network
import socket
import ujson
import time

# Příklad dat pro demonstraci.
list_pp = [1, 2, 3, "test"]
mat_pp = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
toup_pp = {"player_pos": (5, 3), "score": 100}

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP-AP", password="protabulesa", authmode=network.AUTH_WPA2_PSK)
# Předpokládá existenci objektu 'display'.
# display.set_pixel(5, 5, "green")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))
s.listen(1)

print(f"Server running! | IP: {ap.ifconfig()[0]}")

while True:
    print("Waiting for a connection...")
    conn, addr = s.accept()
    conn.settimeout(5.0) # Nastavení timeoutu pro operace se socketem
    print(f"Client connected from: {addr}")
    
    # Proměnná pro ukládání dat od klienta
    client_data = {}
    host_message_counter = 0

    try:
        while True:
            # 1. PŘÍJEM DAT OD KLIENTA
            try:
                line = conn.readline()
                if not line:
                    print("Client disconnected gracefully.")
                    break
                
                client_data = ujson.loads(line)
                print(f"Received from client: {client_data}")
                
            except (ValueError, KeyError) as e:
                print(f"Error parsing JSON from client: {e}")
                client_data = {}
            except OSError as e:
                # Při timeoutu nebo jiném selhání čtení
                print(f"Read operation failed: {e}")
                # Můžeme pokračovat v posílání dat
            
            # 2. ODESLÁNÍ DAT KLIENTOVI
            # Změna zprávy pro demonstraci
            host_message_counter += 1
            host_message = f"Zprava od hosta c. {host_message_counter}"
            
            data_to_send = {
                "list_pp": list_pp,
                "mat_pp": mat_pp,
                "toup_pp": toup_pp,
                "host_message": host_message,
                "received_client_input": client_data.get('user_input', 'No input yet')
            }
            
            serialized_data = ujson.dumps(data_to_send) + '\n'
            conn.sendall(serialized_data.encode('utf-8'))
            
            time.sleep(1) # Pomalujeme komunikaci pro lepší čitelnost v konzoli

    except OSError as e:
        print(f"Connection with {addr} lost: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed. Ready for next client.")