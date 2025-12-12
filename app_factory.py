# # app_factory.py - ACTUALIZADO CON MEJORAS DE SEGURIDAD
# import os
# from flask import Flask
# from extensions import db, login_manager, migrate, csrf, mail
# from dotenv import load_dotenv

# load_dotenv()  # Cargar variables de entorno

# def create_app():
#     from dotenv import load_dotenv
#     load_dotenv()  # 👈 AGREGAR ESTA LÍNEA
    
#     app = Flask(__name__)
    
#     # Configuración
#     app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'fallback-secret-key-change-in-production')
    
#     # Base de datos - PostgreSQL de Replit
#     database_url = os.environ.get('DATABASE_URL')
#     if database_url:
#         app.config['SQLALCHEMY_DATABASE_URI'] = database_url
#     else:
#         # Fallback a MySQL local para desarrollo
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sitex_prueba'
    
#     app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#         'pool_recycle': 300,
#         'pool_pre_ping': True,
#     }
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # Configuración de correo para recuperación de contraseña
#     app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
#     app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
#     app.config['MAIL_USE_TLS'] = True
#     app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
#     app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#     app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@hayuelos.com')
    
#     # Configuración de uploads
#     app.config['UPLOAD_FOLDER'] = 'static/uploads'
#     app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
#     app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
#     # Inicializar extensiones
#     db.init_app(app)
#     login_manager.init_app(app)
#     migrate.init_app(app, db)
#     csrf.init_app(app)
#     mail.init_app(app)
    
#     # Configuración de login_manager
#     login_manager.login_view = 'auth.login'
#     login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
#     login_manager.login_message_category = 'warning'
    
#     # Cargador de usuario
#     @login_manager.user_loader
#     def load_user(user_id):
#         from models import Empleado
#         empleado = db.session.get(Empleado, int(user_id))
#         # Verificar si el usuario está activo
#         if empleado and not empleado.activo:
#             return None
#         return empleado
    
#     # Registrar blueprints
#     from routes import auth_bp, main_bp, dashboard_bp, medicion_bp, admin_bp
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(main_bp)
#     app.register_blueprint(dashboard_bp)
#     app.register_blueprint(medicion_bp)
#     app.register_blueprint(admin_bp)
    
#     # Crear tablas y datos iniciales
#     with app.app_context():
#         db.create_all()
        
#         from models import Empleado, Tanque
#         # Verificar si ya hay tanques
#         if db.session.query(Tanque).count() == 0:
#             tanque1 = Tanque(tipo_combustible='Diesel', capacidad=6000, activo=True)
#             tanque2 = Tanque(tipo_combustible='Diesel', capacidad=12000, activo=True)
#             tanque3 = Tanque(tipo_combustible='ACPM', capacidad=12000, activo=True)
#             tanque4 = Tanque(tipo_combustible='Extra', capacidad=6000, activo=True)

#             db.session.add_all([tanque1, tanque2, tanque3, tanque4])
#             db.session.commit()
#             print("✓ Tanques creados")
    
#     # Protección contra XSS en templates
#     @app.after_request
#     def set_secure_headers(response):
#         response.headers['X-Content-Type-Options'] = 'nosniff'
#         response.headers['X-Frame-Options'] = 'SAMEORIGIN'
#         response.headers['X-XSS-Protection'] = '1; mode=block'
#         return response
    
#     return app


# app_factory.py - OPTIMIZADO PARA VERCEL
import os
from flask import Flask
from extensions import db, login_manager, migrate, csrf, mail
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración general
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')

    # Configuración base de datos - CORREGIDA PARA VERCEL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Fallback para desarrollo local
        database_url = 'mysql+pymysql://root:@localhost/sitex_prueba'
    else:
        # Convertir mysql:// a mysql+pymysql:// si es necesario
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de correo
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@sitex.com')
    
    # Configuración uploads
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Config login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Cargador de usuario
    @login_manager.user_loader
    def load_user(user_id):
        from models import Empleado
        empleado = db.session.get(Empleado, int(user_id))
        if empleado and not empleado.activo:
            return None
        return empleado
    
    # Blueprints
    from routes import auth_bp, main_bp, dashboard_bp, medicion_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicion_bp)
    app.register_blueprint(admin_bp)
    
    # Crear tablas solo en desarrollo - NO en Vercel
    with app.app_context():
        try:
            db.create_all()
            
            from models import Tanque
            if db.session.query(Tanque).count() == 0:
                tanques = [
                    Tanque(tipo_combustible='Diesel', capacidad=6000, activo=True),
                    Tanque(tipo_combustible='Diesel', capacidad=12000, activo=True),
                    Tanque(tipo_combustible='ACPM', capacidad=12000, activo=True),
                    Tanque(tipo_combustible='Extra', capacidad=6000, activo=True)
                ]
                db.session.add_all(tanques)
                db.session.commit()
                print("✓ Tanques creados")
        except Exception as e:
            print(f"Error al crear tablas: {e}")

    @app.after_request
    def set_secure_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
