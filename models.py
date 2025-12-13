# models.py - ACTUALIZADO CON CONFIRMACIÓN DE EMAIL
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
from extensions import db
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import bcrypt

class Empleado(db.Model, UserMixin):
    __tablename__ = 'empleado'
    id_empleados = db.Column(db.Integer, primary_key=True)
    nombre_empleado = db.Column(db.String(30), nullable=False)
    apellido_empleado = db.Column(db.String(30), nullable=False)
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    tipo_documento = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(45))
    cargo_establecido = db.Column(db.String(45))
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    temporal = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)
    
    # NUEVOS CAMPOS PARA CONFIRMACIÓN DE EMAIL
    email_confirmado = db.Column(db.Boolean, default=False)
    token_confirmacion = db.Column(db.String(100))
    token_confirmacion_expiry = db.Column(db.DateTime)
    
    # Recuperación de contraseña
    reset_token = db.Column(db.String(100))
    reset_token_expiry = db.Column(db.DateTime)
    
    aceptado_terminos = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    descargues = db.relationship("Descargue", back_populates="empleado", lazy=True)
    mediciones_cargue = db.relationship("MedicionCargue", back_populates="empleado", lazy=True)
    registro_medidas = db.relationship("RegistroMedida", back_populates="empleado", lazy=True)
    pedidos_combustible = db.relationship("PedidoCombustible", back_populates="empleado", lazy=True)
    documentos = db.relationship("Documento", back_populates="empleado", lazy=True)
    sesiones_activas = db.relationship("SesionActiva", back_populates="empleado", lazy=True)
    acciones_auditoria = db.relationship("Auditoria", back_populates="empleado", lazy=True)

    def get_id(self):
        return str(self.id_empleados)

    @property
    def idEmpleados(self):
        return self.id_empleados

    @property
    def rol(self):
        return self.cargo_establecido

    @property
    def confirmado(self):
        return self.email_confirmado

    @property
    def is_active(self):
        return self.activo and self.email_confirmado

    def __repr__(self):
        return f'<Empleado {self.nombre_empleado} {self.apellido_empleado}>'

    def check_password(self, raw_password):
        import bcrypt
        if not getattr(self, 'contrasena', None):
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.contrasena.encode('utf-8'))

    @property
    def is_locked(self):
        return not self.activo

    # NUEVO: Generar token de confirmación de email
    def generate_confirmation_token(self, hours_valid=24):
        token = secrets.token_urlsafe(48)
        self.token_confirmacion = token
        self.token_confirmacion_expiry = datetime.utcnow() + timedelta(hours=hours_valid)
        return token

    # NUEVO: Verificar token de confirmación
    def verify_confirmation_token(self, token):
        if not self.token_confirmacion or self.token_confirmacion != token:
            return False
        if not getattr(self, 'token_confirmacion_expiry', None):
            return False
        return datetime.utcnow() < self.token_confirmacion_expiry


    # NUEVO: Confirmar email
    def confirmar_email(self):
        self.email_confirmado = True
        self.token_confirmacion = None
        self.token_confirmacion_expiry = None

    def generate_reset_token(self):
        """Generar token de recuperación de contraseña"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token):
        """Verificar token de recuperación"""
        if self.reset_token == token and self.reset_token_expiry > datetime.utcnow():
            return True
        return False
    
    def set_password(self, raw_password: str):
        self.contrasena = bcrypt.hashpw(
            raw_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        if not self.contrasena:
            return False
        try:
            return bcrypt.checkpw(
                raw_password.encode("utf-8"),
                self.contrasena.encode("utf-8")
            )
        except ValueError:
            # hash corrupto o heredado
            return False

class SesionActiva(db.Model):
    """Tabla para rastrear sesiones activas"""
    __tablename__ = 'sesiones_activas'
    id_sesion = db.Column(db.Integer, primary_key=True)
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actividad = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    activa = db.Column(db.Boolean, default=True)
    
    empleado = db.relationship("Empleado", back_populates="sesiones_activas")


class Auditoria(db.Model):
    """Tabla de auditoría para rastrear cambios"""
    __tablename__ = 'auditoria'
    id_auditoria = db.Column(db.Integer, primary_key=True)
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    accion = db.Column(db.String(50))
    tabla = db.Column(db.String(50))
    registro_id = db.Column(db.Integer)
    datos_anteriores = db.Column(db.Text)
    datos_nuevos = db.Column(db.Text)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    empleado = db.relationship("Empleado", back_populates="acciones_auditoria")


# models.py - SECCIÓN DE TANQUE CORREGIDA

class Tanque(db.Model):
    __tablename__ = 'tanques'
    id_tanques = db.Column(db.Integer, primary_key=True)
    tipo_combustible = db.Column(db.String(45))
    capacidad = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Altura máxima permitida en cm
    altura_maxima_cm = db.Column(db.Float, default=0.0)
    
    # Radio del tanque en cm
    radio_cm = db.Column(db.Float, default=125.0)

    mediciones_cargue = db.relationship("MedicionCargue", back_populates="tanque", lazy=True)
    registro_medidas = db.relationship("RegistroMedida", back_populates="tanque", lazy=True)
    ventas = db.relationship("Venta", back_populates="tanque", lazy=True)

    @property
    def idTanques(self):
        return self.id_tanques

    @property
    def capacidad_gal(self):
        return self.capacidad or 0

    @property
    def contenido(self):
        """Obtener contenido actual del tanque en galones"""
        ultima_medicion = RegistroMedida.query.filter_by(
            id_tanques=self.id_tanques
        ).order_by(RegistroMedida.fecha_hora_registro.desc()).first()
        
        if ultima_medicion and ultima_medicion.galones:
            return float(ultima_medicion.galones)
        return 0.0

    @property
    def altura_actual_cm(self):
        """Obtener altura actual en cm basada en última medición"""
        ultima_medicion = RegistroMedida.query.filter_by(
            id_tanques=self.id_tanques
        ).order_by(RegistroMedida.fecha_hora_registro.desc()).first()
        
        if not ultima_medicion or not ultima_medicion.medida_combustible:
            return 0.0
        
        try:
            return float(ultima_medicion.medida_combustible)
        except (ValueError, TypeError):
            return 0.0

    @property
    def porcentaje_llenado(self):
        """Porcentaje de llenado del tanque"""
        capacidad = self.capacidad or 0
        contenido = self.contenido or 0
        
        if capacidad > 0:
            return (contenido / capacidad) * 100
        return 0.0
    
    @property
    def volumen_m3(self):
        """Volumen en metros cúbicos"""
        capacidad = self.capacidad or 0
        return round(capacidad * 3.78541 / 1000, 2)

    @property
    def diametro_m(self):
        """Diámetro en metros"""
        radio_cm = self.radio_cm or 125.0
        return (radio_cm * 2) / 100

    @property
    def altura_m(self):
        """Altura máxima en metros"""
        altura_maxima = self.altura_maxima_cm or 0.0
        return altura_maxima / 100

    def validar_medicion(self, medida_cm):
        """Validar que una medición no exceda la altura máxima"""
        altura_max = self.altura_maxima_cm or 0
        if medida_cm > altura_max:
            return False, f"Medida excede altura máxima del tanque ({altura_max} cm)"
        return True, "OK"

    def cm_a_galones(self, altura_cm):
        """Convertir altura en cm a galones para este tanque específico"""
        radio = self.radio_cm or 125.0
        if radio <= 0:
            return 0
        
        # Volumen = π * r² * h
        area_base = 3.14159 * (radio ** 2)
        volumen_cm3 = area_base * altura_cm
        
        # 1 galón = 3785.411784 cm³
        galones = volumen_cm3 / 3785.411784
        
        return round(galones, 2)

    def __repr__(self):
        return f'<Tanque {self.tipo_combustible} - {self.capacidad} gal>'


class Descargue(db.Model):
    __tablename__ = 'descargues'
    idDescargue = db.Column(db.Integer, primary_key=True)
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'), nullable=False)
    empleado = db.relationship("Empleado", back_populates="descargues")

    medida_inicial_cm = db.Column(db.Numeric(10, 2))
    medida_inicial_gl = db.Column(db.Numeric(10, 2))
    descargue_cm = db.Column(db.Numeric(10, 2))
    descargue_gl = db.Column(db.Numeric(10, 2))
    medida_final_cm = db.Column(db.Numeric(10, 2))
    medida_final_gl = db.Column(db.Numeric(10, 2))
    diferencia = db.Column(db.Numeric(10, 2))
    tanque = db.Column(db.String(50))
    observaciones1 = db.Column(db.String(255))
    observaciones2 = db.Column(db.String(255))
    kit_derrames = db.Column(db.String(5))
    extintores = db.Column(db.String(5))
    conos = db.Column(db.String(5))
    boquillas = db.Column(db.String(5))
    botas = db.Column(db.String(5))
    gafas = db.Column(db.String(5))
    tapaoidos = db.Column(db.String(5))
    guantes = db.Column(db.String(5))
    brillante = db.Column(db.String(5))
    traslucido = db.Column(db.String(5))
    claro = db.Column(db.String(5))
    solidos = db.Column(db.String(5))
    separacion = db.Column(db.String(50))
    fecha = db.Column(db.Date)
    imagen_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<Descargue {self.tanque} - {self.fecha}>'


class MedicionCargue(db.Model):
    __tablename__ = 'medicion_cargue'
    id_medicion_cargue = db.Column(db.Integer, primary_key=True)
    medida_anterior = db.Column(db.String(45))
    medida_posterior = db.Column(db.String(45))
    formato_de_entrega = db.Column(db.String(45))
    galones_totales = db.Column(db.String(45))
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    empleado = db.relationship("Empleado", back_populates="mediciones_cargue")
    tanque = db.relationship("Tanque", back_populates="mediciones_cargue")

    @property
    def idMedicion_cargue(self):
        return self.id_medicion_cargue

    @property
    def idEmpleados(self):
        return self.id_empleados

    @property
    def idTanques(self):
        return self.id_tanques

    def __repr__(self):
        return f'<MedicionCargue {self.galones_totales} - {self.fecha}>'


class RegistroMedida(db.Model):
    __tablename__ = 'registro_medidas'
    id_registro_medidas = db.Column(db.Integer, primary_key=True)
    medida_combustible = db.Column(db.String(45))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    fecha_hora_registro = db.Column(db.DateTime)
    galones = db.Column(db.Integer)
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    novedad = db.Column(db.String(255))
    tipo_medida = db.Column(db.String(30), default='rutinario')
    imagen_path = db.Column(db.String(255))

    empleado = db.relationship("Empleado", back_populates="registro_medidas")
    tanque = db.relationship("Tanque", back_populates="registro_medidas")

    @property
    def idRegistro_medidas(self):
        return self.id_registro_medidas

    @property
    def idEmpleados(self):
        return self.id_empleados

    @property
    def idTanques(self):
        return self.id_tanques

    def __repr__(self):
        return f'<RegistroMedida {self.galones} gal - {self.fecha_hora_registro}>'


class PedidoCombustible(db.Model):
    __tablename__ = 'pedido_combustible'
    idPedido_Combustible = db.Column(db.Integer, primary_key=True)
    galones_acpm = db.Column(db.String(45))
    galones_corriente = db.Column(db.String(45))
    galones_extra = db.Column(db.String(45))
    total_galones = db.Column(db.String(45))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))

    empleado = db.relationship("Empleado", back_populates="pedidos_combustible")

    def __repr__(self):
        return f'<PedidoCombustible {self.total_galones} gal>'


class Documento(db.Model):
    __tablename__ = 'documento'
    idDocumento = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(100))
    fecha_informe = db.Column(db.Date)
    tipo_documento_informe = db.Column(db.String(45))
    tipo_medicion = db.Column(db.String(45))
    fecha_descargue = db.Column(db.Date)
    id_empleado = db.Column(db.String(45))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    revision_vehiculo = db.Column(db.String(3))
    revision_conductor = db.Column(db.String(3))
    medida_inicial = db.Column(db.String(45))
    cantidad_descargue = db.Column(db.String(45))
    medida_final = db.Column(db.String(45))
    diferencias = db.Column(db.String(45))
    id_registro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.id_registro_medidas'))

    empleado = db.relationship("Empleado", back_populates="documentos")
    adjuntos = db.relationship("DocumentoAdjunto", backref="documento", lazy=True)
    historial = db.relationship("DocumentoHistorial", backref="documento", lazy=True)

    def __repr__(self):
        return f'<Documento {self.nombre_documento}>'


class DocumentoAdjunto(db.Model):
    __tablename__ = 'documento_adjunto'
    idAdjunto = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, db.ForeignKey('documento.idDocumento'))
    nombre_archivo = db.Column(db.String(100))
    url_archivo = db.Column(db.Text)
    fecha_subida = db.Column(db.DateTime)


class DocumentoHistorial(db.Model):
    __tablename__ = 'documento_historial'
    idHistorial = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, db.ForeignKey('documento.idDocumento'))
    fecha_evento = db.Column(db.DateTime)
    descripcion_evento = db.Column(db.String(255))
    usuario_responsable = db.Column(db.String(45))


class DocumentoTipo(db.Model):
    __tablename__ = 'documento_tipo'
    idTipoDocumento = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(45))


class Venta(db.Model):
    __tablename__ = 'ventas'
    idVenta = db.Column(db.Integer, primary_key=True)
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    cantidad_galones = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    tanque = db.relationship("Tanque", back_populates="ventas")

    def __repr__(self):
        return f'<Venta {self.cantidad_galones} gal - {self.fecha}>'


class InicioSesion(db.Model):
    __tablename__ = 'inicio_de_sesion'
    userNumDoc = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255))
    temporal = db.Column(db.Boolean, default=False)


class InicioSesionEmpleado(db.Model):
    __tablename__ = 'inicio_de_sesion_has_empleado'
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'), primary_key=True)
    userNumDoc = db.Column(db.String(20), db.ForeignKey('inicio_de_sesion.userNumDoc'), primary_key=True)


class RegistroMedidaMedicionCargue(db.Model):
    __tablename__ = 'registro_medidas_has_medicion_cargue'
    id_registro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.id_registro_medidas'), primary_key=True)
    id_medicion_cargue = db.Column(db.Integer, db.ForeignKey('medicion_cargue.id_medicion_cargue'), primary_key=True)
