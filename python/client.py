from dependencies import *

# Connect the client to the server

def connection_to_server():
    host = "127.0.0.1"
    port = 65432

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("connected to server")

    except ConnectionRefusedError:
        print("Error: connection refused")

    finally:
        client_socket.close()

if __name__ == "main":
    connection_to_server()