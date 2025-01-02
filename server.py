import socket
import threading

# List to keep track of client connections
clients = []
# List to store client names
client_names = []

def broadcast(message, client):
    """Send the message to all clients except the sender"""
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)

def handle_client(client, address):
    """Handles communication with the client"""
    print(f"New connection: {address}")
    
    # Request and store client name
    client.send("Enter your name: ".encode('utf-8'))
    name = client.recv(1024).decode('utf-8')
    client_names.append(name)
    clients.append(client)
    print(f"Client {name} connected from {address}")

    # Broadcast a welcome message
    broadcast(f"{name} has joined the chat!".encode('utf-8'), client)

    # Keep listening for incoming messages from the client
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(f"{name}: {message.decode('utf-8')}".encode('utf-8'), client)
        except:
            break

    # Remove the client and broadcast a leave message
    clients.remove(client)
    client_names.remove(name)
    broadcast(f"{name} has left the chat.".encode('utf-8'), client)
    client.close()

def start_server():
    """Set up and run the server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Listening on port 5555
    server.listen(5)
    print("Server started on port 5555")

    while True:
        client, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

if __name__ == "__main__":
    start_server()
