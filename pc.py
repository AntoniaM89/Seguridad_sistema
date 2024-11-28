from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

#ENCRYPTION_KEY = base64.b64decode("Y4sdD5naWqLQTfTBwWQs1SVWIz/77pPpUrvFF8ZTo78=")

app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, resources={r"/login": {"origins": "*"}})

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Avril.8989!',
    database='Seguridad'
)

cursor = db.cursor()
"""
def decrypt_chacha20(nonce, ciphertext):
    cipher = Cipher(algorithms.ChaCha20(ENCRYPTION_KEY, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)
"""
@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del cuerpo de la solicitud
    data = request.json  
    correo = data.get('correo')
    contrasena= data.get('contrasena')
#    contrasena_encrypted = data.get('contrasena')

    # Verificar si la contraseña está presente
#    if not contrasena_encrypted:
#        return jsonify({'error': 'La contraseña es obligatoria'}), 400

#    try:
        # Intentar separar el nonce y el ciphertext
#        nonce, ciphertext = contrasena_encrypted.split(':')
#        print('Datos recibidos en /login:')
#        print('Correo:', correo)
#        print('Contrasena:', contrasena_encrypted)

        # Decodificar los valores base64
#        nonce = base64.b64decode(nonce)
#        ciphertext = base64.b64decode(ciphertext)

#        print('Nonce decodificado:', nonce)
#        print('Ciphertext decodificado:', ciphertext)

        # Verificar que el nonce tiene el tamaño correcto (16 bytes)
        #if len(nonce) != 16:
        #    return jsonify({'error': 'El nonce debe tener 16 bytes'}), 400

        # Desencriptar la contraseña
#        contrasena = decrypt_chacha20(nonce, ciphertext).decode()

#        print(f"Contraseña descifrada: {contrasena}")  # Imprimir la contraseña descifrada

#    except Exception as e:
#        print(f"Error al procesar la contraseña: {e}")
#        return jsonify({'error': 'Error al procesar la contraseña', 'details': str(e)}), 400

    # Verificar que los datos necesarios estén presentes
#    if not correo or not contrasena:
#        return jsonify({'error': 'El correo y la contraseña son obligatorios'}), 400

    #try:
        # Realizar la consulta de login en la base de datos
    cursor.execute("SELECT correo, contrasena FROM login WHERE correo = %s AND contrasena = %s",(correo, contrasena))
    login_result = cursor.fetchone()
    if login_result:
        return jsonify({'message': 'Login exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    #except mysql.connector.Error as err:
    print(f"Error en la consulta de login: {err}")
    return jsonify({'error': 'Error al procesar el login'}), 500

@app.route('/register', methods=['POST'])
def register():
    # Obtener los datos del cuerpo de la solicitud
    data = request.json  
    print(f"Datos recibidos en /register: {data}") 
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    #nonce = data.get('nonce')
    #ciphertext = data.get('ciphertext')
    """
    if not nonce or not ciphertext:
        return jsonify({'error': 'El nonce y el ciphertext son obligatorios'}), 400

    try:
        # Decodificar los valores base64
        nonce = base64.b64decode(nonce)
        ciphertext = base64.b64decode(ciphertext)

        print('Nonce decodificado:', nonce)
        print('Ciphertext decodificado:', ciphertext)

        # Verificar que el nonce tiene el tamaño correcto (16 bytes)
        if len(nonce) != 16:
            return jsonify({'error': 'El nonce debe tener 16 bytes'}), 400

        # Desencriptar la contraseña
        contrasena = decrypt_chacha20(nonce, ciphertext).decode()

    except Exception as e:
        print(f"Error al procesar la contraseña: {e}")
        return jsonify({'error': 'Error al procesar la contraseña', 'details': str(e)}), 400

    # Verificar que los datos necesarios estén presentes
    if not nombre or not correo or not contrasena:
        return jsonify({'error': 'El nombre, correo y contraseña son obligatorios'}), 400
    """
    try:
        # Insertar el usuario en la base de datos
        cursor.execute("INSERT INTO login (nombre, correo, contrasena) VALUES (%s, %s, %s)",(nombre, correo, contrasena))
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