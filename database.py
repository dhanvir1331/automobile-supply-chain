# database.py
from sqlalchemy.orm import Session
from models import Order, SessionLocal

def create_order(db: Session, customer_order: str):
    db_order = Order(customer_order=customer_order, status="Pending", processed_by="Customer")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: str, processed_by: str):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db_order.processed_by = processed_by
        db.commit()
        db.refresh(db_order)
    return db_order

def get_pending_orders(db: Session):
    return db.query(Order).filter(Order.status == "Pending").all()
