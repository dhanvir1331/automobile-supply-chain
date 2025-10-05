from models import RawMaterial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///supply_chain.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def populate_raw_materials():
    materials = [
        {"material_name": "Steel", "quantity_available": 5},
        {"material_name": "Glass", "quantity_available": 4},
        {"material_name": "Plastic", "quantity_available": 3},
        {"material_name": "Leather", "quantity_available": 2},
    ]

    db = SessionLocal()
    for material in materials:
        raw_material = RawMaterial(
            material_name=material["material_name"],
            quantity_available=material["quantity_available"],
        )
        db.add(raw_material)

    db.commit()
    db.close()
    print("Raw materials populated successfully.")


populate_raw_materials()
