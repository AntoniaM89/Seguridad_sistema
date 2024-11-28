import os
import base64

# Generar una clave de 32 bytes (256 bits) aleatoria
key = os.urandom(32)

# Convertir la clave a formato Base64
key_base64 = base64.b64encode(key).decode()

print("Tu clave Base64 es:", key_base64)