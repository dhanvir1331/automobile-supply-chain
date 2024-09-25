import socket
import tkinter as tk
import threading
from sqlalchemy.orm import Session
from database import get_pending_orders, update_order_status, SessionLocal

order_queue = []

def receive_order():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                order_id, order, status = message.split(':')
                if status == "Manufactured":
                    db = SessionLocal()
                    db_order = update_order_status(db, int(order_id), "In Distribution", "Distributor")
                    order_queue.append(db_order)
                    update_order_listbox()
                    process_button.config(state="normal")
                intermediary_listbox.insert(tk.END, f"Order ID: {order_id} - Status: {status}")
        except:
            break

def update_order_listbox():
    order_listbox.delete(0, tk.END)
    for order in order_queue:
        order_listbox.insert(tk.END, f"Order ID: {order.id} - {order.customer_order}")

def process_order():
    if order_queue:
        processed_order = order_queue.pop(0)
        order_listbox.delete(0)
        client_socket.send(f"{processed_order.id}:{processed_order.customer_order}:Distributed".encode('utf-8'))
        update_order_status(SessionLocal(), processed_order.id, "Processed", "Distributor")
        update_order_listbox()
    if not order_queue:
        process_button.config(state="disabled")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.12.84.250', 5555))
client_socket.send('distributor'.encode('utf-8'))

root = tk.Tk()
root.title("Distributor Client")
root.configure(bg='#2E2E2E')

frame = tk.Frame(root, bg='#2E2E2E')
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

left_frame = tk.Frame(frame, bg='#2E2E2E')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

order_listbox = tk.Listbox(left_frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
order_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

process_button = tk.Button(left_frame, text="Process Order", command=process_order, relief='flat', font=('Helvetica', 12), fg='#FFFFFF', bg='#007ACC')
process_button.pack(pady=(10, 0))

right_frame = tk.Frame(frame, bg='#2E2E2E', width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

intermediary_listbox = tk.Listbox(right_frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#007ACC', font=('Helvetica', 12))
intermediary_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

thread = threading.Thread(target=receive_order)
thread.start()

root.mainloop()
