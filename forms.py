# forms.py - ACTUALIZADO CON MEJORAS
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, DecimalField, DateField, IntegerField, SubmitField, FileField as WTFileField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, EqualTo, ValidationError
from datetime import date

class LoginForm(FlaskForm):
    username = StringField("Usuario o Documento *", validators=[DataRequired(message="Campo obligatorio")], 
                         render_kw={"placeholder": "Ingrese su usuario o documento"})
    password = PasswordField("Contraseña *", validators=[DataRequired(message="Campo obligatorio")],
                           render_kw={"placeholder": "Ingrese su contraseña"})
    remember_me = BooleanField("Recuérdame")
    submit = SubmitField("Iniciar Sesión")

class RegisterForm(FlaskForm):
    nombre_empleado = StringField("Nombre *", validators=[DataRequired(message="Campo obligatorio"), Length(max=30)],
                                render_kw={"placeholder": "Ingrese su nombre"})
    apellido_empleado = StringField("Apellido *", validators=[DataRequired(message="Campo obligatorio"), Length(max=30)],
                                   render_kw={"placeholder": "Ingrese su apellido"})
    numero_documento = StringField("Número de Documento *", validators=[DataRequired(message="Campo obligatorio"), Length(max=20)],
                                  render_kw={"placeholder": "Número de documento"})
    tipo_documento = SelectField("Tipo Documento *", choices=[
        ("CC", "Cédula"), ("CE", "Cédula Extranjería"), ("TI", "Tarjeta Identidad")
    ], validators=[DataRequired(message="Campo obligatorio")])
    email = StringField("Email *", validators=[DataRequired(message="Campo obligatorio"), Email(message="Email inválido"), Length(max=45)],
                      render_kw={"placeholder": "ejemplo@correo.com"})
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=15)],
                         render_kw={"placeholder": "Teléfono"})
    direccion = StringField("Dirección", validators=[Optional(), Length(max=45)],
                          render_kw={"placeholder": "Dirección"})
    usuario = StringField("Usuario *", validators=[DataRequired(message="Campo obligatorio"), Length(max=15)],
                        render_kw={"placeholder": "Nombre de usuario"})
    cargo_establecido = SelectField(
        "Cargo *",
        choices=[("islero", "Islero"), ("encargado", "Encargado"), ("admin", "Administrador")],
        validators=[DataRequired(message="Campo obligatorio")]
    )
    aceptar_terminos = BooleanField("Acepto los términos y condiciones y la política de privacidad *", 
                                   validators=[DataRequired(message="Debe aceptar los términos")])
    submit = SubmitField("Registrarse")

class MedicionForm(FlaskForm):
    """Formulario de medición - SOLO RUTINARIO"""
    medida_combustible = StringField('Medida (cm) *', 
        validators=[DataRequired(message="Campo obligatorio")],
        render_kw={"placeholder": "Medida en cm"})
    
    galones = DecimalField('Galones', 
        validators=[Optional()],
        places=2,
        render_kw={"readonly": True, "id": "galones"})
    
    tanque = SelectField('Tanque *', 
        coerce=int, 
        validators=[DataRequired(message="Campo obligatorio")])
    
    # SOLO RUTINARIO - sin opciones de cargue/descargue
    tipo_medida = SelectField('Tipo de Medición *',
        choices=[('rutinario', 'Rutinario')],  # Solo rutinario
        default='rutinario',
        validators=[DataRequired(message="Campo obligatorio")])
    
    novedad = TextAreaField('Novedad', 
        validators=[Optional(), Length(max=255)],
        render_kw={"placeholder": "Observaciones adicionales", "rows": 3})
    
    imagen = FileField('Foto de Factura', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Solo imágenes o PDF')])
    
    submit = SubmitField("Guardar Medición")


class DescargueForm(FlaskForm):
    """Formulario de descargue con selectores de tanque"""
    tanque = SelectField('Tanque *',  # Cambiado a SelectField
        coerce=int,
        validators=[DataRequired(message="Campo obligatorio")])
    
    medida_inicial_cm = DecimalField('Medida Inicial (cm) *', 
        validators=[DataRequired(message="Campo obligatorio")], 
        places=2)
    
    medida_inicial_gl = DecimalField('Medida Inicial (gl)', 
        validators=[Optional()], 
        places=2)
    
    descargue_cm = DecimalField('Descargue (cm) *', 
        validators=[DataRequired(message="Campo obligatorio")], 
        places=2)
    
    descargue_gl = DecimalField('Descargue (gl)', 
        validators=[Optional()], 
        places=2)
    
    medida_final_cm = DecimalField('Medida Final (cm)', 
        validators=[Optional()], 
        places=2)
    
    medida_final_gl = DecimalField('Medida Final (gl)', 
        validators=[Optional()], 
        places=2)
    
    diferencia = DecimalField('Diferencia', 
        validators=[Optional()], 
        places=2)
    
    # Seguridad del conductor - checkboxes en el template
    botas = SelectField('Botas *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    gafas = SelectField('Gafas *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    tapaoidos = SelectField('Tapaoídos *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    guantes = SelectField('Guantes *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    # Seguridad del vehículo
    kit_derrames = SelectField('Kit Derrames *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    extintores = SelectField('Extintores *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    conos = SelectField('Conos *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    boquillas = SelectField('Boquillas *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    # Calidad del combustible con botones ON/OFF
    brillante = SelectField('Brillante *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    traslucido = SelectField('Traslúcido *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    claro = SelectField('Claro *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='si')
    
    solidos = SelectField('Sólidos *', 
        choices=[('si', 'Sí'), ('no', 'No')], 
        default='no')
    
    separacion = StringField('Separación', 
        validators=[Optional(), Length(max=50)])
    
    observaciones1 = TextAreaField('Observaciones 1', 
        validators=[Optional(), Length(max=255)])
    
    observaciones2 = TextAreaField('Observaciones 2', 
        validators=[Optional(), Length(max=255)])
    
    fecha = DateField('Fecha', 
        validators=[Optional()], 
        default=date.today)
    
    imagen = FileField('Foto de Factura', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Solo imágenes o PDF')])
    
    submit = SubmitField("Registrar Descargue")


class CargueEmergenciaForm(FlaskForm):
    """NUEVO: Formulario para cargue de emergencia"""
    tanque = SelectField('Tanque *',
        coerce=int,
        validators=[DataRequired(message="Campo obligatorio")])
    
    medida_anterior = StringField('Medida Anterior (cm) *',
        validators=[DataRequired(message="Campo obligatorio")],
        render_kw={"placeholder": "Medida antes del cargue"})
    
    medida_posterior = StringField('Medida Posterior (cm) *',
        validators=[DataRequired(message="Campo obligatorio")],
        render_kw={"placeholder": "Medida después del cargue"})
    
    formato_entrega = SelectField('Formato de Entrega *',
        choices=[
            ('pipa', 'Pipa'),
            ('camion', 'Camión'),
            ('otro', 'Otro')
        ],
        validators=[DataRequired(message="Campo obligatorio")])
    
    galones_totales = DecimalField('Galones Totales *',
        validators=[DataRequired(message="Campo obligatorio")],
        places=2,
        render_kw={"placeholder": "Total de galones cargados"})
    
    observaciones = TextAreaField('Observaciones',
        validators=[Optional(), Length(max=255)],
        render_kw={"rows": 3, "placeholder": "Detalles del cargue de emergencia"})
    
    imagen = FileField('Foto del Remito/Factura',
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], 'Solo imágenes o PDF')])
    
    submit = SubmitField("Registrar Cargue de Emergencia")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Contraseña Actual *', validators=[DataRequired(message="Campo obligatorio")],
                                   render_kw={"placeholder": "Contraseña actual"})
    new_password = PasswordField('Nueva Contraseña *', validators=[DataRequired(message="Campo obligatorio"), Length(min=6, message="Mínimo 6 caracteres")],
                               render_kw={"placeholder": "Nueva contraseña (mín. 6 caracteres)"})
    confirm_password = PasswordField('Confirmar Contraseña *', 
                                   validators=[DataRequired(message="Campo obligatorio"), EqualTo('new_password', message='Las contraseñas deben coincidir')],
                                   render_kw={"placeholder": "Confirmar nueva contraseña"})
    submit = SubmitField('Cambiar Contraseña')

class ResetPasswordForm(FlaskForm):
    submit = SubmitField('Resetear')

class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(message="Campo obligatorio"), Email(message="Email inválido")],
                      render_kw={"placeholder": "ejemplo@correo.com"})
    submit = SubmitField('Enviar Enlace de Recuperación')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Nueva Contraseña *', validators=[DataRequired(message="Campo obligatorio"), Length(min=6, message="Mínimo 6 caracteres")],
                           render_kw={"placeholder": "Nueva contraseña (mín. 6 caracteres)"})
    confirm_password = PasswordField('Confirmar Contraseña *',
                                   validators=[DataRequired(message="Campo obligatorio"), EqualTo('password', message='Las contraseñas deben coincidir')],
                                   render_kw={"placeholder": "Confirmar nueva contraseña"})
    submit = SubmitField('Restablecer Contraseña')

class TanqueForm(FlaskForm):
    tipo_combustible = StringField('Tipo de Combustible *', validators=[DataRequired(message="Campo obligatorio"), Length(max=45)],
                                  render_kw={"placeholder": "Diesel, ACPM, Extra, etc."})
    capacidad = IntegerField('Capacidad (galones) *', validators=[DataRequired(message="Campo obligatorio"), NumberRange(min=1, message="Debe ser mayor a 0")],
                           render_kw={"placeholder": "Capacidad en galones"})
    activo = BooleanField('Tanque Activo', default=True)
    submit = SubmitField('Guardar Tanque')

class CargaMasivaForm(FlaskForm):
    archivo = FileField('Archivo CSV/Excel *', validators=[
        DataRequired(message="Debe seleccionar un archivo"),
        FileAllowed(['csv', 'xlsx', 'xls'], 'Solo archivos CSV o Excel')
    ])
    tipo_carga = SelectField('Tipo de Carga *', choices=[
        ('empleados', 'Empleados'),
        ('tanques', 'Tanques'),
        ('mediciones', 'Mediciones')
    ], validators=[DataRequired(message="Campo obligatorio")])
    submit = SubmitField('Cargar Datos')

class FiltroMedicionesForm(FlaskForm):
    fecha_desde = DateField('Desde', validators=[Optional()])
    fecha_hasta = DateField('Hasta', validators=[Optional()])
    tanque = SelectField('Tanque', coerce=int, validators=[Optional()])
    tipo_medida = SelectField('Tipo', choices=[('', 'Todos'), ('rutinario', 'Rutinario'), ('cargue', 'Cargue'), ('descargue', 'Descargue')],
                            validators=[Optional()])
    empleado = SelectField('Empleado', coerce=int, validators=[Optional()])
    submit = SubmitField('Filtrar')
