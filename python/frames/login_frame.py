import socket
import threading
import customtkinter as ctk
from python.dependencies import get_contacts, send_message, get_user_id, check_credentials, add_user
from python.frames.chat_frame import ChatFrame


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, conn):
        super().__init__(parent)
        self.controller = controller
        self.conn = conn

        self.configure(fg_color="#F7E6D4")

        self.login_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.login_frame, text="LAN Chat", font=("Arial", 24, "bold"), text_color="#58C7DE"
        )
        self.title_label.pack(pady=(20, 5))

        self.username_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Username", width=250, corner_radius=10, height=40
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Password", width=250, corner_radius=10, height=40, show="*"
        )
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(
            self.login_frame, text="Login", command=self.handle_login, width=250, corner_radius=10
        )
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(
            self.login_frame, text="Register", command=self.handle_register, width=250, corner_radius=10
        )
        self.register_button.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if check_credentials(username, password, self.controller.conn):
            self.controller.username = username

            # Create the socket connection here
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 65433))  # Connect to the server (use the correct IP and port)

            # Send the username to the server
            client_socket.send(username.encode('utf-8'))

            # Pass the socket along with other arguments to the ChatFrame
            self.controller.show_frame(ChatFrame, username=username, client_socket=client_socket)
        else:
            print("Invalid username or password.")

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Make sure both username and password are provided
        if username and password:
            if add_user(username, password, self.controller.conn):
                print(f"User {username} registered successfully.")
            else:
                print("Registration failed.")
        else:
            print("Please provide both a username and a password.")
