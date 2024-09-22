import socket
import tkinter as tk
from tkinter import ttk
import threading
from sqlalchemy.orm import Session
from database import create_order, SessionLocal

def send_purchase_order():
    selected_order = order_combobox.get()
    db = SessionLocal()
    db_order = create_order(db, selected_order)
    client_socket.send(f"{db_order.id}:{selected_order}:Ordered".encode('utf-8'))
    response_label.config(text=f"Order Placed: {selected_order}")
    order_combobox.set('')  # Clear the selection

def receive_notifications():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                order_id, order, status = message.split(':')
                notification_listbox.insert(tk.END, f"Order ID: {order_id} - Status: {status}")
                intermediary_listbox.insert(tk.END, f"Order ID: {order_id} - Status: {status}")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555))
client_socket.send('customer'.encode('utf-8'))

root = tk.Tk()
root.title("Customer Client")
root.configure(bg='#2E2E2E')

frame = tk.Frame(root, bg='#2E2E2E')
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

left_frame = tk.Frame(frame, bg='#2E2E2E')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Dropdown (Combobox) for Toyota car selection
order_options = ["Toyota Camry", "Toyota Corolla", "Toyota RAV4", "Toyota Highlander", "Toyota Tacoma"]
order_combobox = ttk.Combobox(left_frame, values=order_options, state='readonly', width=20)
order_combobox.pack(pady=(0, 10))

send_button = tk.Button(left_frame, text="Place Order", command=send_purchase_order, relief='flat', font=('Helvetica', 12), fg='#FFFFFF', bg='#007ACC')
send_button.pack(pady=(0, 10))

response_label = tk.Label(left_frame, text="", bg='#2E2E2E', fg='#FFFFFF')
response_label.pack(pady=(0, 10))

notification_listbox = tk.Listbox(left_frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
notification_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

right_frame = tk.Frame(frame, bg='#2E2E2E', width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

intermediary_listbox = tk.Listbox(right_frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
intermediary_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

thread = threading.Thread(target=receive_notifications)
thread.start()

root.mainloop()
