import socket
import tkinter as tk
from tkinter import messagebox
import threading
from sqlalchemy.orm import Session
from database import get_pending_orders, update_order_status, check_raw_materials, SessionLocal
from models import RawMaterial

order_queue = []

def receive_order():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                order_id, order, status = message.split(':')
                if status == "Ordered":
                    db = SessionLocal()
                    db_order = update_order_status(db, int(order_id), "In Manufacturing", "Manufacturing")
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
        processed_order = order_queue[0]  # Check the first order in the queue
        if check_raw_materials(processed_order.customer_order):  # Check if raw materials are sufficient
            # Deduct raw materials
            deduct_raw_materials(processed_order.customer_order)
            order_queue.pop(0)
            order_listbox.delete(0)
            client_socket.send(f"{processed_order.id}:{processed_order.customer_order}:Manufactured".encode('utf-8'))
            update_order_status(SessionLocal(), processed_order.id, "Processed", "Manufacturing")
            update_order_listbox()
            intermediary_listbox.insert(tk.END, f"Order ID: {processed_order.id} Manufactured.")
        else:
            tk.messagebox.showwarning("Insufficient Materials", f"Cannot process Order. Insufficient raw materials.")
    if not order_queue:
        process_button.config(state="disabled")

def deduct_raw_materials(car_model):
    required_materials = {
        "Toyota Camry": ["Steel", "Glass", "Plastic"],
        "Toyota Corolla": ["Steel", "Glass", "Plastic"],
        "Toyota RAV4": ["Steel", "Glass", "Plastic", "Leather"],
        "Toyota Highlander": ["Steel", "Glass", "Plastic", "Leather"],
        "Toyota Tacoma": ["Steel", "Glass", "Plastic"]
    }
    
    materials_needed = required_materials.get(car_model, [])
    db = SessionLocal()
    
    for material in materials_needed:
        raw_material = db.query(RawMaterial).filter(RawMaterial.material_name == material).one()
        raw_material.quantity_available -= 1  # Deduct one unit for each material
        db.add(raw_material)

    db.commit()
    db.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.12.84.250', 5555))
client_socket.send('manufacturing'.encode('utf-8'))

root = tk.Tk()
root.title("Manufacturing Client")
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
