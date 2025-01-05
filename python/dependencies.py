import psycopg2
from psycopg2.extras import RealDictCursor

def establish_connection():
    try:
        conn = psycopg2.connect(
            database="LAN-CHAT-APP",
            user="postgres",
            password="Pangbourne4!",
            host="localhost",
            port="5432"
        )
        print("Database connection established.")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def check_credentials(username, password, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result and result[0] == password
    except Exception as e:
        print(f"Error checking credentials: {e}")
        return False

def add_user(username, password, conn):
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def get_user_id(username, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"Error retrieving user ID: {e}")
        return None

def get_contacts(conn, username):
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT u.id, u.username 
                FROM users u
                WHERE u.username != %s
            """
            cursor.execute(query, (username,))
            results = cursor.fetchall()
            return [{"id": row[0], "username": row[1]} for row in results]
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return []

def send_message(sender_id, chat_id, message, conn):
    try:
        # First, check if the chat exists
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM chats WHERE id = %s", (chat_id,))
            result = cursor.fetchone()

            # If the chat doesn't exist, create it
            if result is None:
                cursor.execute("INSERT INTO chats (id) VALUES (%s)", (chat_id,))
                conn.commit()

        # Now, insert the message into the messages table
        with conn.cursor() as cursor:
            query = """
                INSERT INTO messages (sender_id, chat_id, content, timestamp)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (sender_id, chat_id, message))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error sending message to the database: {e}")
        return False
