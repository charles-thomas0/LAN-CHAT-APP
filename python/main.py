import customtkinter as ctk
from frames.login_frame import LoginFrame
from frames.chat_frame import ChatFrame
from python.dependencies import establish_connection


class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_frame = None
        self.title("LAN Chat App")
        self.geometry("600x400")

        # Establish database connection
        self.conn = establish_connection()

        # Container for frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # Dictionary to store frames
        self.show_frame(LoginFrame)  # Show login frame initially

    def show_frame(self, frame_class, *args, **kwargs):
        # Destroy current frame only if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        # Create and display the new frame
        self.current_frame = frame_class(self.container, self, conn=self.conn, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()