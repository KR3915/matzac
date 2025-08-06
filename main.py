from logic import *
import network
import socket
import ujson  # For serializing data
import time

# Example data for demonstration.
# In your code, these would be populated dynamically.
list_pp = [1, 2, 3, "test"]
mat_pp = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
toup_pp = {"player_pos": (5, 3), "score": 100}

ap = network.WLAN(network.AP_IF)
ap.active(True)
# Using 'essid' which is standard, and a network constant for authmode.
ap.config(essid="ESP-AP", password="protabulesa", authmode=network.AUTH_WPA2_PSK)
display.set_pixel(5, 5, "green")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1234))  # Bind to all available interfaces
s.listen(1)

print(f"Server running! | IP: {ap.ifconfig()[0]}")

while True:
    # Wait for a client to connect. This is a blocking call.
    print("Waiting for a connection...")
    conn, addr = s.accept()
    print(f"Client connected from: {addr}")
    try:
        # This loop continuously sends data to the connected client
        while True:
            # In a real application, you would update your variables here.
            # For this example, we'll just use the static ones.
            # e.g., toup_pp['score'] += 1

            data_to_send = {
                "list_pp": list_pp,
                "mat_pp": mat_pp,
                "toup_pp": toup_pp,
            }

            # Serialize data and add a newline to act as a message delimiter
            # for the receiver to easily split messages.
            serialized_data = ujson.dumps(data_to_send) + '\n'

            conn.sendall(serialized_data.encode('utf-8'))

            # Wait for 0.1 seconds to send 10 times per second
            time.sleep(0.1)

    except OSError as e:
        # This will happen if the client disconnects.
        print(f"Connection with {addr} lost: {e}")
    finally:
        # Ensure the connection is closed when the inner loop breaks or an error occurs.
        conn.close()
        print(f"Connection with {addr} closed. Ready for next client.")
