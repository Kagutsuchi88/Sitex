# seed_db.py - Crear tablas e insertar tanques iniciales
# Uso: python seed_db.py

from app_factory import create_app
from extensions import db
from models import Tanque

app = create_app()

with app.app_context():
    # Si prefieres usar migraciones, evita create_all en producción.
    db.create_all()

    if db.session.query(Tanque).count() == 0:
        tanque1 = Tanque(tipo_combustible='Diesel', capacidad=6000, activo=True)
        tanque2 = Tanque(tipo_combustible='Diesel', capacidad=12000, activo=True)
        tanque3 = Tanque(tipo_combustible='ACPM', capacidad=12000, activo=True)
        tanque4 = Tanque(tipo_combustible='Extra', capacidad=6000, activo=True)

        db.session.add_all([tanque1, tanque2, tanque3, tanque4])
        db.session.commit()
        print("✓ Tanques creados")
    else:
        print("Tanques ya existen, no se añadió nada.")