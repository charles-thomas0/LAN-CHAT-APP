from dependencies import *

# Listen for connections

def start_server():
    host = "127.0.0.1"
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"server is open and listening for connections on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"connected to {client_address}")
        client_socket.close()

# Sync with DB

def fetch_messages():
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * from messages;")
        messages = cursor.fetchall()
        cursor.close()
        connection.close()
        return messages
    return

# Test with DB


def test_server_db_connection():
    conn = db_connection()
    if conn:
        print("server connected")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * from messages;")
            result = cursor.fetchone()
            print(result)
        finally:
            conn.close()
            print("connection closed")

if __name__ == "__main__":
    start_server()
