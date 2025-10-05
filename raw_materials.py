from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import RawMaterial

DATABASE_URL = "sqlite:///supply_chain.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def display_raw_materials():
    db = SessionLocal()
    raw_materials = db.query(RawMaterial).all()

    for material in raw_materials:
        print(
            f"ID: {material.id}, Name: {material.material_name}, Quantity Available: {material.quantity_available}"
        )

    db.close()


display_raw_materials()
