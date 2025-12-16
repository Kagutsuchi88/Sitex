# Hayuelos - Sistema de Gestión de Estación de Servicios

## Overview
Sistema web para gestión de estación de combustible Hayuelos. Incluye autenticación de usuarios, gestión de tanques, mediciones y reportes.

## Tech Stack
- **Backend**: Python 3.11, Flask 3.0.0
- **Database**: PostgreSQL (Replit)
- **Frontend**: Bootstrap 5.3, Jinja2 templates
- **Email**: Gmail SMTP con Flask-Mail

## Project Structure
```
├── main.py              # Entry point
├── app_factory.py       # Flask app factory
├── routes.py            # All routes and blueprints
├── models.py            # SQLAlchemy models
├── forms.py             # WTForms
├── extensions.py        # Flask extensions
├── templates/           # Jinja2 templates
│   ├── auth/           # Login, register, password reset
│   ├── dashboard/      # Main dashboard views
│   ├── admin/          # Admin views
│   └── medicion/       # Measurement views
└── static/             # CSS, images, uploads
```

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (auto-configured)
- `MAIL_USERNAME`: Gmail address for sending emails
- `MAIL_PASSWORD`: Gmail app password (16 characters)
- `SECRET_KEY`: Flask secret key

## Email Configuration
The app uses Gmail SMTP for sending confirmation and password reset emails:
- Server: smtp.gmail.com
- Port: 587
- TLS: Enabled

**Note**: Gmail requires an "App Password" for third-party apps. Generate one at https://myaccount.google.com/apppasswords

## Recent Changes
- 2025-12-16: Estadísticas reducidas a 2 métricas clave (Stock Bajo + Rendimiento Mensual)
- 2025-12-16: Añadido botón para descargar reporte mensual en PDF con gráficas
- 2025-12-16: Paginación de empleados cada 10 registros
- 2025-12-16: Funcionalidad para cambiar rol de empleados desde el listado
- 2025-12-13: Fixed vertical scrolling on login/register pages
- 2025-12-13: Configured PostgreSQL database
- 2025-12-13: Added Gmail SMTP credentials for email functionality

## User Preferences
- Language: Spanish (es)
- Target deployment: Vercel (originally), now Replit
