import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20, width=50)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Message input
        self.message_input = tk.Entry(root, width=40)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)
        self.message_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Initialize socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 5555))  # Connect to the server
            self.start_threads()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            self.root.destroy()

    def start_threads(self):
        """Start threads for receiving messages."""
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def receive_messages(self):
        """Receive messages from the server and display them in the chat window."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.update_chat_display(message)
            except Exception as e:
                self.update_chat_display("Disconnected from the server.")
                break

    def send_message(self, event=None):
        """Send a message to the server."""
        message = self.message_input.get().strip()
        if message:
            self.client.send(message.encode('utf-8'))
            self.message_input.delete(0, tk.END)
            self.update_chat_display(f"You: {message}")

    def update_chat_display(self, message):
        """Update the chat display area."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

# Start the client GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()
