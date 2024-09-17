import socket
import threading

clients = {
    'customer': None,
    'manufacturing': None,
    'distributor': None,
    'showroom': None
}

def handle_client(client_socket, client_type):
    clients[client_type] = client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_type)
        except:
            break

def broadcast(message, sender_type):
    for client_type, socket in clients.items():
        if client_type != sender_type and socket:
            socket.send(message.encode('utf-8'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(5)

while True:
    client_socket, addr = server.accept()
    client_type = client_socket.recv(1024).decode('utf-8')
    threading.Thread(target=handle_client, args=(client_socket, client_type)).start()
