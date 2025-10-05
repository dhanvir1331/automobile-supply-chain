from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
DATABASE_URL = "sqlite:///supply_chain.db"  # Example for SQLite
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Import your RawMaterial model
from models import RawMaterial  # Replace 'your_module' with the actual module name


def display_raw_materials():
    db = SessionLocal()
    raw_materials = db.query(RawMaterial).all()  # Get all rows in RawMaterial table

    for material in raw_materials:
        print(
            f"ID: {material.id}, Name: {material.material_name}, Quantity Available: {material.quantity_available}"
        )

    db.close()


# Call the function to display the materials
display_raw_materials()
