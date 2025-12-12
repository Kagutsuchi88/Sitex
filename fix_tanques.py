# fix_tanques.py - Script para corregir datos de tanques
# Ejecutar: python fix_tanques.py

from app_factory import create_app
from extensions import db
from models import Tanque

def calcular_altura_maxima(capacidad_galones):
    """Calcular altura máxima en cm basada en capacidad del tanque"""
    radio_cm = 125  # 2.5m de diámetro
    
    # Volumen en cm³ = capacidad en galones * 3785.411784
    volumen_cm3 = capacidad_galones * 3785.411784
    
    # Altura = Volumen / (π * r²)
    area_base = 3.14159 * (radio_cm ** 2)
    altura_cm = volumen_cm3 / area_base
    
    return round(altura_cm, 2)

app = create_app()

with app.app_context():
    print("🔧 Corrigiendo datos de tanques...")
    
    tanques = Tanque.query.all()
    
    if not tanques:
        print("❌ No hay tanques en la base de datos")
    else:
        for tanque in tanques:
            # Asegurar que altura_maxima_cm no sea None
            if tanque.altura_maxima_cm is None or tanque.altura_maxima_cm == 0:
                tanque.altura_maxima_cm = calcular_altura_maxima(tanque.capacidad)
                print(f"✅ Tanque {tanque.id_tanques}: altura_maxima_cm = {tanque.altura_maxima_cm}")
            
            # Asegurar que radio_cm no sea None
            if tanque.radio_cm is None or tanque.radio_cm == 0:
                tanque.radio_cm = 125.0
                print(f"✅ Tanque {tanque.id_tanques}: radio_cm = {tanque.radio_cm}")
        
        db.session.commit()
        print(f"\n✅ Se actualizaron {len(tanques)} tanques correctamente")
        
        # Verificar
        print("\n📊 Estado de los tanques:")
        for tanque in tanques:
            print(f"  - Tanque {tanque.id_tanques} ({tanque.tipo_combustible}):")
            print(f"    Capacidad: {tanque.capacidad} gal")
            print(f"    Altura máx: {tanque.altura_maxima_cm} cm")
            print(f"    Radio: {tanque.radio_cm} cm")
            print(f"    Diámetro: {tanque.diametro_m} m")
            print()

print("\n✅ Script completado")