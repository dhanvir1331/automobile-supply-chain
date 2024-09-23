from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import RawMaterial, SessionLocal  # Import your RawMaterial model and SessionLocal

# Function to update the quantity of raw materials
def update_raw_material(material_name, new_quantity):
    db = SessionLocal()
    
    # Query the material by its name
    raw_material = db.query(RawMaterial).filter(RawMaterial.material_name == material_name).first()
    
    if raw_material:
        raw_material.quantity_available = new_quantity
        db.add(raw_material)
        db.commit()
        print(f"Updated {material_name} to {new_quantity} units.")
    else:
        print(f"Material {material_name} not found.")
    
    db.close()

# Example usage: Update materials
def update_all_materials():
    materials_to_update = [
        {"material_name": "Steel", "new_quantity": 5},
        {"material_name": "Glass", "new_quantity": 5},
        {"material_name": "Plastic", "new_quantity": 5},
        {"material_name": "Leather", "new_quantity": 5},
    ]
    
    for material in materials_to_update:
        update_raw_material(material["material_name"], material["new_quantity"])

# Run the update function
if __name__ == "__main__":
    update_all_materials()
