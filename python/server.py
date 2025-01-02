from dependencies import *

# DB config
DB_CONFIG = {
    "database": "LAN-CHAT-APP",
    "user": "postgres",
    "password": "Pangbourne4!",
    "host": "localhost",
    "port": "5432"
}

# Server Config
host = "127.0.0.1"
port = 65432
clients = []  # Map: client_socket -> username


# Save messages to db
def save_message_to_db(sender, message):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (sender, message) VALUES (%s, %s)",
            (sender, message)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")


# Broadcast messages to connected clients
def broadcast_message(sender, message, is_server_message=False):
    if not is_server_message:
        message = f"{sender}: {message}"  # Only prepend for user messages.
    for client in clients:
        try:
            client["socket"].send(message.encode())
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            clients.remove(client)


# Function to handle a client
def handle_client(client_socket, address):
    global clients
    print(f"New connection from {address}")

    # Wait for the username from the client
    username = client_socket.recv(1024).decode("utf-8")
    print(f"{username} has joined the chat.")
    clients.append({"socket": client_socket, "username": username})

    # Broadcast the join message
    broadcast_message("Server", f"{username} has joined the chat!", is_server_message=True)

    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                print(f"Connection closed by {address}")
                break
            print(f"Message from {username}: {data}")

            # Broadcast the message to all other clients
            broadcast_message(username, data)

    except Exception as e:
        print(f"Error with {address}: {e}")
    finally:
        clients = [client for client in clients if client["socket"] != client_socket]
        client_socket.close()
        print(f"Connection with {address} closed.")


# Start the server
def start_server():
    print("Starting server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
