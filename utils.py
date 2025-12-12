# utils.py - ACTUALIZADO CON PERMISOS MEJORADOS PARA ENCARGADO
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from extensions import db
from models import Auditoria
import json


def roles_required(*roles):
    """Decorador para verificar roles con auditoría"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página', 'warning')
                return redirect(url_for('auth.login'))

            rol_usuario = (current_user.cargo_establecido or '').lower().strip()
            roles_lower = [r.lower().strip() for r in roles]

            if rol_usuario not in roles_lower:
                flash(f'No tiene permisos. Se requiere rol: {", ".join(roles)}', 'danger')
                return redirect(url_for('dashboard.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def islero_or_encargado_required(f):
    """Permite que islero Y encargado registren medidas"""
    return roles_required('islero', 'encargado', 'admin')(f)


def admin_or_encargado_required(f):
    """Decorador para admin o encargado - AMBOS TIENEN PERMISOS COMPLETOS"""
    return roles_required('admin', 'encargado')(f)


def admin_required(f):
    """
    Decorador solo para admin Y encargado
    NOTA: Encargado tiene los mismos permisos que admin
    """
    return roles_required('admin', 'encargado')(f)


def encargado_full_access(f):
    """
    Nuevo decorador: Encargado tiene acceso completo (admin + islero)
    """
    return roles_required('admin', 'encargado')(f)


def registrar_auditoria(accion, tabla, registro_id, datos_anteriores=None, datos_nuevos=None):
    """Registrar cambios en la auditoría"""
    try:
        from flask import request
        auditoria = Auditoria(
            id_empleados=current_user.id_empleados if current_user.is_authenticated else None,
            accion=accion,
            tabla=tabla,
            registro_id=registro_id,
            datos_anteriores=json.dumps(datos_anteriores) if datos_anteriores else None,
            datos_nuevos=json.dumps(datos_nuevos) if datos_nuevos else None,
            ip_address=request.remote_addr if request else None
        )
        db.session.add(auditoria)
        db.session.commit()
    except Exception as e:
        print(f"Error al registrar auditoría: {e}")


def allowed_file(filename, allowed_extensions=None):
    """Verificar extensión de archivo"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions