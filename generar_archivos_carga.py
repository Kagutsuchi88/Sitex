import pandas as pd
from datetime import datetime

# --- EMPLEADOS ---
empleados = [
    ["Juan", "Pérez", "12345678", "CC", "juan.perez@hayuelos.com", "3001234567", "Calle 1 #2-3", "Islero", "jperez", "Temp123!", True, True, False],
    ["María", "Gómez", "87654321", "CC", "maria.gomez@hayuelos.com", "3109876543", "Carrera 4 #5-6", "Encargado", "mgomez", "Temp456!", True, True, False],
    ["Carlos", "Rodríguez", "11223344", "CC", "carlos.rodriguez@hayuelos.com", "3201122334", "Transversal 7 #8-9", "Islero", "crodriguez", "Temp789!", True, True, False],
    ["Ana", "López", "99887766", "CC", "ana.lopez@hayuelos.com", "3159988776", "Diagonal 10 #11-12", "Islero", "alopez", "Temp000!", True, True, False],
]
cols_empleados = ["nombre_empleado","apellido_empleado","numero_documento","tipo_documento","email","telefono","direccion","cargo_establecido","usuario","contrasena","temporal","activo","aceptado_terminos"]
pd.DataFrame(empleados, columns=cols_empleados).to_csv("empleados_carga_masiva.csv", index=False)
pd.DataFrame(empleados, columns=cols_empleados).to_excel("empleados_carga_masiva.xlsx", index=False)

# --- TANQUES ---
tanques = [
    ["Diesel", 8000, True],
    ["ACPM", 10000, True],
    ["Extra", 5000, True],
    ["Corriente", 7000, False],
]
cols_tanques = ["tipo_combustible", "capacidad", "activo"]
pd.DataFrame(tanques, columns=cols_tanques).to_csv("tanques_carga_masiva.csv", index=False)
pd.DataFrame(tanques, columns=cols_tanques).to_excel("tanques_carga_masiva.xlsx", index=False)

# --- MEDICIONES ---
mediciones = [
    [1, 45.5, 1200.00, "rutinario", "Nivel estable", "2025-10-28 07:00:00", 2],
    [2, 60.0, 2800.50, "cargue", "Cargue de 3000 gal", "2025-10-28 12:30:00", 3],
    [3, 30.2, 850.75, "rutinario", "Fuga leve detectada", "2025-10-28 18:00:00", 4],
    [1, 44.8, 1180.00, "rutinario", "Nivel bajo", "2025-10-29 07:00:00", 2],
]
cols_mediciones = ["tanque_id","medida_combustible","galones","tipo_medida","novedad","fecha_hora_registro","empleado_id"]
pd.DataFrame(mediciones, columns=cols_mediciones).to_csv("mediciones_carga_masiva.csv", index=False)
pd.DataFrame(mediciones, columns=cols_mediciones).to_excel("mediciones_carga_masiva.xlsx", index=False)

print("Archivos generados: empleados, tanques, mediciones (.csv y .xlsx)")