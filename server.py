import socket
import threading

clients = {
    'customer': None,
    'manufacturing': None,
    'distributor': None,
    'showroom': None
}

order_queue = []  # Queue to track multiple orders

# Handle communication between clients
def handle_client(client_socket, role):
    global order_queue
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{role.capitalize()} received: {message}")
                
                if role == 'customer':
                    order_queue.append(message)  # Add order to queue
                    if clients['manufacturing']:
                        clients['manufacturing'].send(message.encode('utf-8'))
                
                elif role == 'manufacturing':
                    if clients['distributor']:
                        clients['distributor'].send(message.encode('utf-8'))
                
                elif role == 'distributor':
                    if clients['showroom']:
                        clients['showroom'].send(message.encode('utf-8'))
                
                elif role == 'showroom':
                    if clients['customer']:
                        order_completed = order_queue.pop(0)  # Mark order as completed
                        clients['customer'].send(f"Order '{order_completed}' fully processed and ready at showroom".encode('utf-8'))
            else:
                break
        except:
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(5)
    print("Server started... Waiting for connections.")

    while True:
        client_socket, addr = server.accept()
        role = client_socket.recv(1024).decode('utf-8')
        print(f"{role.capitalize()} connected from {addr}")

        clients[role] = client_socket

        thread = threading.Thread(target=handle_client, args=(client_socket, role))
        thread.start()

if __name__ == "__main__":
    start_server()
