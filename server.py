import socket
import threading

clients = {
    "customer": None,
    "manufacturing": None,
    "distributor": None,
    "showroom": None,
}


def handle_client(client_socket, client_type):
    clients[client_type] = client_socket
    print(f"Client connected: {client_type} at {client_socket.getpeername()}")

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Received message from {client_type}: {message}")
                broadcast(message, client_type)
            else:
                print(f"Connection closed by {client_type}")
                break
        except Exception as e:
            print(f"Error handling message from {client_type}: {e}")
            break

    client_socket.close()
    clients[client_type] = None
    print(f"Client disconnected: {client_type} at {client_socket.getpeername()}")


def broadcast(message, sender_type):
    print(f"Broadcasting message from {sender_type}: {message}")
    for client_type, socket in clients.items():
        if client_type != sender_type and socket:
            try:
                socket.send(message.encode("utf-8"))
                print(f"Sent message to {client_type}")
            except Exception as e:
                print(f"Error sending message to {client_type}: {e}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5555))
server.listen(5)
print("Server is listening on port 5555")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    client_type = client_socket.recv(1024).decode("utf-8")
    print(f"Client type received: {client_type}")
    threading.Thread(target=handle_client, args=(client_socket, client_type)).start()
