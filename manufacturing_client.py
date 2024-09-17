import socket
import tkinter as tk
import threading

order_queue = []

def receive_order():
    while True:
        try:
            order = client_socket.recv(1024).decode('utf-8')
            if order:
                order_queue.append(order)
                update_order_listbox()
                process_button.config(state="normal")
        except:
            break

def update_order_listbox():
    order_listbox.delete(0, tk.END)
    for order in order_queue:
        order_listbox.insert(tk.END, order)

def process_order():
    if order_queue:
        processed_order = order_queue.pop(0)
        order_listbox.delete(0)
        client_socket.send(f"Order '{processed_order}' Processed by Manufacturing".encode('utf-8'))
        update_order_listbox()
    if not order_queue:
        process_button.config(state="disabled")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
client_socket.send('manufacturing'.encode('utf-8'))  # Identifies as manufacturing

root = tk.Tk()
root.title("Manufacturing Client")
root.configure(bg='#2E2E2E')

# Layout
frame = tk.Frame(root, bg='#2E2E2E')
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

order_listbox = tk.Listbox(frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
order_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Gradient button
def create_gradient_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, relief='flat', font=('Helvetica', 12), fg='#FFFFFF')
    button.pack(pady=(10, 0))
    button.bind("<Enter>", lambda e: button.config(bg='#0056b3'))
    button.bind("<Leave>", lambda e: button.config(bg='#007ACC'))
    button.config(bg='#007ACC')
    return button

process_button = create_gradient_button(frame, "Process Order", process_order)

# Thread to listen for incoming orders
thread = threading.Thread(target=receive_order)
thread.start()

root.mainloop()
