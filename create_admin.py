# create_admin.py
# Ejecutar desde el entorno del proyecto (donde esté app_factory.py)
# Ejemplo:
# ADMIN_USERNAME=admin ADMIN_NUM_DOC=0000 ADMIN_EMAIL=admin@local ADMIN_PASSWORD=ChangeMe123! python create_admin.py

import os
import bcrypt
from app_factory import create_app
from extensions import db
from models import Empleado

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_NUM_DOC = os.environ.get('ADMIN_NUM_DOC', '0000000000')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@local')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!')

app = create_app()

with app.app_context():
    # Busca por usuario/email/documento
    admin = Empleado.query.filter(
        (Empleado.usuario == ADMIN_USERNAME) |
        (Empleado.email == ADMIN_EMAIL) |
        (Empleado.numero_documento == ADMIN_NUM_DOC)
    ).first()

    hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if admin:
        admin.usuario = ADMIN_USERNAME
        admin.numero_documento = ADMIN_NUM_DOC
        admin.email = ADMIN_EMAIL
        admin.contrasena = hashed
        admin.cargo_establecido = 'admin'
        admin.temporal = False
        admin.activo = True
        admin.aceptado_terminos = True
        print("Admin existente actualizado.")
    else:
        admin = Empleado(
            nombre_empleado='Admin',
            apellido_empleado='Hayuelos',
            numero_documento=ADMIN_NUM_DOC,
            tipo_documento='CC',
            email=ADMIN_EMAIL,
            telefono='',
            direccion='',
            cargo_establecido='admin',
            usuario=ADMIN_USERNAME,
            contrasena=hashed,
            temporal=False,
            activo=True,
            aceptado_terminos=True
        )
        db.session.add(admin)
        print("Admin creado.")

    db.session.commit()
    print("Operación completada. Usuario admin:", ADMIN_USERNAME)