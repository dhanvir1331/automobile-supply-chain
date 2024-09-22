# database.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import Order, RawMaterial, SessionLocal

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

def check_raw_materials(car_model):
    required_materials = {
        "Toyota Camry": ["Steel", "Glass", "Plastic"],
        "Toyota Corolla": ["Steel", "Glass", "Plastic"],
        "Toyota RAV4": ["Steel", "Glass", "Plastic", "Leather"],
        "Toyota Highlander": ["Steel", "Glass", "Plastic", "Leather"],
        "Toyota Tacoma": ["Steel", "Glass", "Plastic"]
    }
    
    # Assuming we have a session already created
    db = SessionLocal()
    
    materials_needed = required_materials.get(car_model, [])
    if not materials_needed:
        return True  # No materials required for unrecognized models
    
    for material in materials_needed:
        try:
            raw_material = db.query(RawMaterial).filter(RawMaterial.material_name == material).one()
            if raw_material.quantity_available <= 0:
                return False  # Insufficient material
        except NoResultFound:
            return False  # Material not found in the inventory
    
    return True  # All required materials are available

def check_inventory_levels(threshold=100):
    db = SessionLocal()
    low_materials = db.query(RawMaterial).filter(RawMaterial.quantity_available < threshold).all()
    db.close()
    
    if low_materials:
        for material in low_materials:
            print(f"Warning: {material.material_name} is low (Available: {material.quantity_available})")
    else:
        print("All materials are above the threshold.")
