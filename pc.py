from flask import Flask, request, jsonify, make_response
import mysql.connector
from flask_cors import CORS
import hashlib
import os
import uuid

app = Flask(__name__)

# Configuración de CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

# Conexión a la base de datos
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Avril.8989!',
    database='Seguridad'
)
cursor = db.cursor()

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    print(f"Datos recibidos en /login: {request.json}")
    data = request.get_json()
    correo = data.get('Lcorreo')
    contrasena = data.get('Lcontrasena')

    try:
        # Verificar si el correo existe en la base de datos
        cursor.execute("SELECT id, nombre, hashed, salt, bloqueado, intentos FROM login WHERE correoh=%s", (correo,))
        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        user_id, nombre, stored_hashed, stored_salt_hex, bloqueado, intentos = user_data

        if bloqueado:
            return jsonify({'error': 'Cuenta bloqueada. Contacte al administrador'}), 403

        # Asegurarse de que el salt es un string antes de usar fromhex
        if isinstance(stored_salt_hex, bytes):
            stored_salt_hex = stored_salt_hex.decode('utf-8')  # Decodificar a string

        stored_salt = bytes.fromhex(stored_salt_hex)
        hashed_attempt = hashlib.sha256(stored_salt + contrasena.encode('utf-8')).hexdigest().upper()

        if hashed_attempt == stored_hashed:
            session_id = str(uuid.uuid4())  # Generar un ID de sesión único
            cursor.execute("UPDATE login SET session_id=%s, intentos=0 WHERE id=%s", (session_id, user_id))
            db.commit()

            response = make_response(jsonify({'message': 'Inicio de sesión exitoso', 'nombre': nombre}), 200)
            response.set_cookie('session_id', session_id, httponly=True, max_age=3600)  # Cookie segura (1 hora)
            return response
        else:
            intentos += 1
            cursor.execute("UPDATE login SET intentos=%s WHERE correoh=%s", (intentos, correo))
            db.commit()

            if intentos >= 3:
                cursor.execute("UPDATE login SET bloqueado=1 WHERE correoh=%s", (correo,))
                db.commit()
                return jsonify({'error': 'Cuenta bloqueada por múltiples intentos fallidos'}), 403

            return jsonify({'error': f'Credenciales inválidas. Intentos restantes: {3 - intentos}'}), 401
    except Exception as err:
        return jsonify({'error': f'Error inesperado: {err}'}), 500

# Ruta de registro
@app.route('/register', methods=['POST'])
def register():
    # Obtener los datos del cuerpo de la solicitud
    data = request.get_json()
    print(f"Datos recibidos en /register: {data}")
    nombre = data.get('Nnombre')
    correo = data.get('CorreoSN')
    correoh = data.get('NNcorreo')  # Correo hashed
    contrasena = data.get('NNcontrasena')

    # Generar salt y hashear la contraseña con el salt
    salt = os.urandom(16)
    salt_hex = salt.hex()
    hashed = hashlib.sha256(salt + contrasena.encode('utf-8')).hexdigest().upper()

    try:
        # Insertar el usuario en la base de datos
        cursor.execute("INSERT INTO login (nombre, correo, correoh, hashed, salt, intentos, bloqueado, session_id) VALUES (%s, %s, %s, %s, %s, 0, 0, '0')",
                       (nombre, correo, correoh, hashed, salt_hex))
        db.commit()  # Confirmar los cambios
        return jsonify({'message': 'Usuario creado exitosamente'}), 201
    except mysql.connector.IntegrityError as err:
        print(f"Error de integridad: {err}")
        return jsonify({'error': 'El correo ya está registrado'}), 400
    except mysql.connector.Error as err:
        print(f"Error al insertar en la base de datos: {err}")
        return jsonify({'error': 'Error al crear el usuario'}), 500


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
