import socket
import tkinter as tk
import threading

def send_purchase_order():
    order = entry.get()
    client_socket.send(order.encode('utf-8'))
    response_label.config(text=f"Order Placed: {order}")
    entry.delete(0, tk.END)

def receive_notification():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                notification_listbox.insert(tk.END, f"Notification: {message}")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
client_socket.send('customer'.encode('utf-8'))  # Identifies as customer

root = tk.Tk()
root.title("Customer Client")
root.configure(bg='#2E2E2E')

# Layout
frame = tk.Frame(root, bg='#2E2E2E')
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

entry = tk.Entry(frame, bg='#1E1E1E', fg='#FFFFFF', borderwidth=2, relief='solid')
entry.pack(pady=(0, 10), fill=tk.X, padx=10)

# Gradient button
def create_gradient_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, relief='flat', font=('Helvetica', 12), fg='#FFFFFF')
    button.pack(pady=(0, 10))
    button.bind("<Enter>", lambda e: button.config(bg='#0056b3'))
    button.bind("<Leave>", lambda e: button.config(bg='#007ACC'))
    button.config(bg='#007ACC')
    return button

send_button = create_gradient_button(frame, "Place Order", send_purchase_order)

response_label = tk.Label(frame, text="", bg='#2E2E2E', fg='#FFFFFF')
response_label.pack(pady=(0, 10))

notification_listbox = tk.Listbox(frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
notification_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Thread to listen for server notifications
thread = threading.Thread(target=receive_notification)
thread.start()

root.mainloop()
