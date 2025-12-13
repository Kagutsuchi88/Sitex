# main.py
from app_factory import create_app

app = create_app()  # ← ¡ESTO ES LO QUE FALTA!

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask, jsonify
# from flask_cors import CORS
# import mysql.connector

# app = Flask(__name__)
# CORS(app)

# def conectar_bd():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='sitex_prueba'
#     )

# @app.route('/api/tanques', methods=['GET'])
# def obtener_tanques():
#     conexion = conectar_bd()
#     cursor = conexion.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM tanques")
#     resultados = cursor.fetchall()
#     cursor.close()
#     conexion.close()
#     return jsonify(resultados)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)