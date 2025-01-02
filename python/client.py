from dependencies import *
import customtkinter as ctk
import threading
import socket

# Constants
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

# Global variables
client_socket = None
username = None


# GUI Class
class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LAN Chat Application")
        self.geometry("600x600")

        # Login Frame
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill="both", expand=True)

        self.login_label = ctk.CTkLabel(self.login_frame, text="Enter your username:")
        self.login_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login)
        self.login_button.pack(pady=10)

        # Chat Frame (hidden until login)
        self.chat_frame = ctk.CTkFrame(self)
        self.messages_textbox = ctk.CTkTextbox(self.chat_frame, width=550, height=400, state="disabled")
        self.messages_textbox.pack(pady=10)

        self.message_entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Type your message here...", width=400)
        self.message_entry.pack(side="left", padx=10, pady=10)

        # Bind the Enter key to send_message
        self.message_entry.bind("<Return>", self.send_message_with_event)

        self.send_button = ctk.CTkButton(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=10, pady=10)

    def send_message_with_event(self, event):
        self.send_message()

    def handle_login(self):
        """Handle user login and switch to the chat window."""
        global username
        username = self.username_entry.get().strip()
        if not username:
            print("Username cannot be empty.")
            return

        if connect_to_server():  # Reuse the connect logic
            self.login_frame.pack_forget()
            self.chat_frame.pack(fill="both", expand=True)
            client_socket.send(username.encode('utf-8'))  # Send username to server

            # Start listening for incoming messages
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
        else:
            print("Failed to connect to the server.")

    def listen_for_messages(self):
        """Listen for messages from the server and display them in the chat."""
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message:
                    self.display_message(message)
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def display_message(self, message):
        """Add a new message to the chat display."""
        self.messages_textbox.configure(state="normal")  # Enable text box to add messages
        self.messages_textbox.insert("end", f"{message}\n")
        self.messages_textbox.configure(state="disabled")  # Disable text box to prevent user input
        self.messages_textbox.see("end")  # Auto-scroll to the bottom

    def send_message(self):
        """Send a message to the server."""
        message = self.message_entry.get().strip()
        if message:
            try:
                client_socket.send(message.encode("utf-8"))
                self.message_entry.delete(0, "end")  # Clear input box
            except Exception as e:
                print(f"Error sending message: {e}")


# Reuse the connect logic from the prototype
def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")
        return True
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return False


# Start the application
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
