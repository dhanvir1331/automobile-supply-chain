from database import (
    RawMaterial,
    SessionLocal,
)


def increment_raw_material(material_name, increment_quantity):
    db = SessionLocal()

    raw_material = (
        db.query(RawMaterial).filter(RawMaterial.material_name == material_name).first()
    )

    if raw_material:
        raw_material.quantity_available += increment_quantity  # Increment the quantity
        db.add(raw_material)
        db.commit()
        print(
            f"Incremented {material_name} by {increment_quantity} units. New quantity: {raw_material.quantity_available}"
        )
    else:
        print(f"Material {material_name} not found.")

    db.close()


def increment_all_materials():
    materials_to_increment = [
        {"material_name": "Steel", "increment_quantity": 5},
        {"material_name": "Glass", "increment_quantity": 5},
        {"material_name": "Plastic", "increment_quantity": 5},
        {"material_name": "Leather", "increment_quantity": 5},
    ]

    for material in materials_to_increment:
        increment_raw_material(
            material["material_name"], material["increment_quantity"]
        )


if __name__ == "__main__":
    increment_all_materials()
