import threading
import customtkinter as ctk
from python.dependencies import get_contacts, send_message as send_message_to_db

class ChatFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, conn, username, client_socket):
        super().__init__(parent)
        self.controller = controller
        self.conn = conn
        self.username = username
        self.client_socket = client_socket

        # Contacts Frame
        self.contacts_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.contacts_frame.pack(side="left", fill="y", padx=10, pady=10, expand=False)

        # Contacts List (using CTkScrollableFrame)
        self.contacts_list = ctk.CTkScrollableFrame(self.contacts_frame, width=200, height=400)
        self.contacts_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate contacts
        self.populate_contacts()

        # Chat Frame
        self.chat_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Chat Textbox
        self.chat_textbox = ctk.CTkTextbox(self.chat_frame, height=25, width=25, state="disabled")
        self.chat_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Message Entry
        self.message_entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Type your message here...")
        self.message_entry.pack(fill="x", padx=10, pady=10)

        # Send Button
        self.send_button = ctk.CTkButton(self.chat_frame, text="Send", command=self.send_message_to_contact)
        self.send_button.pack(pady=10)

        # Start a thread to listen for incoming messages
        self.listen_thread = threading.Thread(target=self.listen_for_messages)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    self.chat_textbox.configure(state="normal")
                    self.chat_textbox.insert("end", f"{message}\n")
                    self.chat_textbox.configure(state="disabled")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def populate_contacts(self):
        contacts = get_contacts(self.controller.conn, self.controller.username)
        for contact in contacts:
            button = ctk.CTkButton(self.contacts_list, text=contact['username'], command=lambda c=contact: self.select_contact(c))
            button.pack(fill="x", padx=5, pady=5)

    def select_contact(self, contact):
        self.current_contact = contact
        self.chat_textbox.configure(state="normal")
        self.chat_textbox.delete("1.0", "end")
        self.chat_textbox.insert("end", f"Chatting with {contact['username']}\n")
        self.chat_textbox.configure(state="disabled")

    def send_message_to_contact(self):
        message = self.message_entry.get().strip()
        if message and self.current_contact:
            sender_id = 1  # Replace with actual current user ID
            chat_id = self.current_contact['id']  # Use the contact's ID as the chat ID
            if send_message_to_db(sender_id, chat_id, message, self.controller.conn):
                self.chat_textbox.configure(state="normal")
                self.chat_textbox.insert("end", f"You: {message}\n")
                self.chat_textbox.configure(state="disabled")
                self.message_entry.delete(0, "end")
                # Send the message to the server
                self.client_socket.send(message.encode('utf-8'))
            else:
                print("Error sending message!")