from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import hashlib
import os
from datetime import timedelta

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

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
    data = request.get_json()
    correo = data.get('Lcorreo')
    contrasena = data.get('Lcontrasena')

    try:
        # Verificar si el correo existe en la base de datos
        cursor.execute("SELECT nombre, hashed, salt, bloqueado, intentos FROM login WHERE correoh=%s", (correo,))
        user_data = cursor.fetchone()

        # Si no se encuentra el usuario
        if not user_data:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Desempaquetar los datos del usuario
        nombre, stored_hashed, stored_salt_hex, bloqueado, intentos = user_data

        # Verificar si la cuenta está bloqueada
        if bloqueado:
            return jsonify({'error': 'Cuenta bloqueada. Contacte al administrador'}), 403

        # Verificar si stored_salt_hex es de tipo bytes, y convertirlo a str si es necesario
        if isinstance(stored_salt_hex, bytes):
            stored_salt_hex = stored_salt_hex.decode('utf-8')

        # Convertir el salt desde hex a bytes
        stored_salt = bytes.fromhex(stored_salt_hex)

        print(f"Salt recuperado: {stored_salt}")
        print(f"Contrasena recibida: {contrasena}")

        # Calcular el hash utilizando el salt y la contraseña
        hashed_attempt = hashlib.sha256(stored_salt + contrasena.encode('utf-8')).hexdigest().upper()

        print(f"Hash calculado: {hashed_attempt}")
        print(f"Hash almacenado: {stored_hashed}")

        # Comparar el hash calculado con el hash almacenado
        if hashed_attempt == stored_hashed:
            # Si el hash coincide, iniciar sesión exitoso, restablecer intentos fallidos
            cursor.execute("UPDATE login SET intentos=0 WHERE correoh=%s", (correo,))
            db.commit()
            return jsonify({'message': 'Inicio de sesión exitoso', 'nombre': nombre}), 200
        else:
            # Si no coincide, incrementar intentos fallidos
            intentos += 1
            cursor.execute("UPDATE login SET intentos=%s WHERE correoh=%s", (intentos, correo))
            db.commit()

            # Si se alcanzan 3 intentos fallidos, bloquear la cuenta
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
