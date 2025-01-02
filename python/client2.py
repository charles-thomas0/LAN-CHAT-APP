from dependencies import *

# Constants
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

# Global variables
client_socket = None
username = None

def listen_for_messages():
    # Continuously listen for messages from the server.
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                # If message is from the server (e.g., join messages)
                if message.startswith("Server:"):
                    print(f"\n{Fore.YELLOW}{message}{Fore.RESET}")
                elif message.startswith(f"{username}:"):
                    continue  # Skip displaying your own messages
                else:
                    # Display messages from other users
                    print(f"\n{Fore.CYAN}{message}{Fore.RESET}")
                # After displaying the message, print the input prompt again
                print(f"{username}> ", end="", flush=True)  # Print prompt on the same line
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_messages():
    # Send messages to the server.
    while True:
        message = input(f"{username}> ")
        if message.lower() == "exit":
            print("Exiting chat.")
            client_socket.close()
            break
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def register_username():
    # Prompt the user to enter a username and send it to the server.
    global username
    username = input("Enter your username: ").strip()
    while not username:
        username = input("Username cannot be empty. Enter your username: ").strip()
    try:
        client_socket.send(username.encode('utf-8'))
    except Exception as e:
        print(f"Error sending username: {e}")

def connect_to_server():
    # Connect to the server.
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")
        return True
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return False

def start_client():
    # Start the client.
    if not connect_to_server():
        return

    register_username()

    # Start a thread to listen for messages from the server
    threading.Thread(target=listen_for_messages, daemon=True).start()

    # Main thread handles sending messages
    send_messages()

if __name__ == "__main__":
    start_client()
