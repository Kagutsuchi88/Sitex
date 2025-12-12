# test_email.py
# Script para probar la configuración de envío de emails
# Ejecutar: python test_email.py

import os
from flask_mail import Message
from app_factory import create_app
from extensions import mail

def test_email_config():
    """Verificar configuración de email"""
    print("=" * 60)
    print("🔍 VERIFICANDO CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        print(f"✅ MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"✅ MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"✅ MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
        print(f"✅ MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"✅ MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
        
        if not app.config.get('MAIL_USERNAME'):
            print("\n❌ ERROR: MAIL_USERNAME no está configurado")
            print("Configura las variables de entorno MAIL_USERNAME y MAIL_PASSWORD")
            return False
        
        return True

def send_test_email(recipient_email):
    """Enviar un email de prueba"""
    print("\n" + "=" * 60)
    print(f"📧 ENVIANDO EMAIL DE PRUEBA A: {recipient_email}")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            msg = Message(
                "✅ Prueba de Email - Sitex",
                recipients=[recipient_email]
            )
            
            msg.body = """
            ¡Hola!
            
            Este es un email de prueba del sistema Hayuelos.
            
            Si recibes este mensaje, significa que la configuración de correo está funcionando correctamente.
            
            Detalles de la prueba:
            - Sistema: Hayuelos - Estación de Servicios
            - Funcionalidad: Confirmación de Email y Recuperación de Contraseña
            - Estado: ✅ Operativo
            
            Saludos,
            Sistema Hayuelos
            """
            
            msg.html = """
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #E10000;">✅ Email de Prueba</h2>
                    <p><strong>¡Hola!</strong></p>
                    <p>Este es un email de prueba del sistema Hayuelos.</p>
                    
                    <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 5px solid #28a745;">
                        <p style="margin: 0;"><strong>✅ ¡Configuración Exitosa!</strong></p>
                        <p style="margin: 5px 0 0 0;">Si recibes este mensaje, el envío de emails está funcionando correctamente.</p>
                    </div>
                    
                    <h3 style="color: #E10000;">Detalles de la Prueba:</h3>
                    <ul>
                        <li>Sistema: Hayuelos - Estación de Servicios</li>
                        <li>Funcionalidad: Confirmación de Email y Recuperación de Contraseña</li>
                        <li>Estado: <span style="color: #28a745;">✅ Operativo</span></li>
                    </ul>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                    <p style="color: #999; font-size: 0.8em; text-align: center;">
                        Sistema Hayuelos - "Y También vendemos combustible"
                    </p>
                </div>
            </body>
            </html>
            """
            
            mail.send(msg)
            print("✅ Email enviado exitosamente!")
            print(f"📬 Revisa la bandeja de entrada de: {recipient_email}")
            print("💡 También revisa la carpeta de spam/correo no deseado")
            return True
            
        except Exception as e:
            print(f"❌ ERROR al enviar email: {str(e)}")
            print("\n🔧 SOLUCIONES POSIBLES:")
            print("1. Verifica que MAIL_USERNAME y MAIL_PASSWORD estén configurados")
            print("2. Si usas Gmail, usa una 'Contraseña de Aplicación'")
            print("3. Verifica que MAIL_SERVER y MAIL_PORT sean correctos")
            print("4. Asegúrate de que no haya firewall bloqueando el puerto 587")
            return False

def test_confirmation_email_format():
    """Probar formato del email de confirmación"""
    print("\n" + "=" * 60)
    print("🎨 PROBANDO FORMATO DE EMAIL DE CONFIRMACIÓN")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        from models import Empleado
        
        # Crear empleado de prueba temporal
        empleado_test = Empleado(
            nombre_empleado="Usuario",
            apellido_empleado="Prueba",
            usuario="test_user",
            numero_documento="12345678",
            email="test@example.com"
        )
        
        token = empleado_test.generate_confirmation_token()
        confirm_url = f"http://localhost:5000/auth/confirm/{token}"
        
        print(f"✅ URL de confirmación generada:")
        print(f"   {confirm_url}")
        print(f"\n✅ Token generado: {token[:20]}...")
        print(f"✅ Expira en: 24 horas")
        
        return True

def main():
    print("\n" + "=" * 60)
    print("🧪 SCRIPT DE PRUEBA - SISTEMA DE EMAILS HAYUELOS")
    print("=" * 60)
    
    # 1. Verificar configuración
    if not test_email_config():
        print("\n❌ Configura las variables de entorno antes de continuar")
        return
    
    # 2. Solicitar email de destino
    print("\n" + "=" * 60)
    recipient = input("📧 Ingresa el email de prueba: ").strip()
    
    if not recipient or '@' not in recipient:
        print("❌ Email inválido")
        return
    
    # 3. Enviar email de prueba
    if send_test_email(recipient):
        print("\n" + "=" * 60)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Revisa tu bandeja de entrada")
        print("2. Si no ves el email, revisa spam/correo no deseado")
        print("3. Si funciona, puedes proceder con el registro de usuarios")
    else:
        print("\n" + "=" * 60)
        print("❌ PRUEBA FALLIDA")
        print("=" * 60)
        print("\n🔧 REVISA:")
        print("1. Variables de entorno (MAIL_USERNAME, MAIL_PASSWORD)")
        print("2. Conexión a internet")
        print("3. Credenciales del servidor SMTP")
    
    # 4. Probar formato de confirmación
    test_confirmation_email_format()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Prueba cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")