import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, login_manager, migrate, csrf, mail

load_dotenv()

def create_app():
    app = Flask(__name__)

    # =========================
    # Configuración básica
    # =========================
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "fallback-secret-key-change-in-production"
    )

    # =========================
    # Base de datos (Railway → Vercel)
    # =========================
    # OBLIGATORIO: DATABASE_URL debe existir
    database_url = os.environ["DATABASE_URL"]

    # SQLAlchemy requiere mysql+pymysql
    if database_url.startswith("mysql://"):
        database_url = database_url.replace(
            "mysql://",
            "mysql+pymysql://",
            1
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Opciones seguras para serverless
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 5,
    }

    # =========================
    # Correo
    # =========================
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "noreply@sitex.com"
    )

    # =========================
    # Uploads
    # =========================
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["ALLOWED_EXTENSIONS"] = {
        "png", "jpg", "jpeg", "gif", "pdf"
    }

    # =========================
    # Inicializar extensiones
    # =========================
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)

    # =========================
    # Login manager
    # =========================
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        from models import Empleado
        empleado = db.session.get(Empleado, int(user_id))
        if empleado and not empleado.activo:
            return None
        return empleado

    # =========================
    # Blueprints
    # =========================
    from routes import (
        auth_bp,
        main_bp,
        dashboard_bp,
        medicion_bp,
        admin_bp,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicion_bp)
    app.register_blueprint(admin_bp)

    # =========================
    # Seguridad básica headers
    # =========================
    @app.after_request
    def set_secure_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    return app
