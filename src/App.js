import './App.css';
import { useState } from 'react';
import nacl from 'tweetnacl';
import naclUtil from 'tweetnacl-util';

function App() {
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [Ncorreo, setNCorreo] = useState("");
  const [Ncontrasena, setNContrasena] = useState("");
  const [Nnombre, setNnombre] = useState("");

  // Validaciones
  const validarInput = (valor) => {
    return !valor.includes("'") && !valor.includes('"') && !valor.includes('=');
  };

  const RestriccionCorreo = (e) => {
    const valor = e.target.value;
    if (validarInput(valor)) {
      setCorreo(valor);
    } else {
      alert('El correo contiene caracteres no permitidos.');
    }
  };

  const RestriccionContrasena = (e) => {
    const valor = e.target.value;
    if (validarInput(valor)) {
      setContrasena(valor);
    } else {
      alert('La contraseña contiene caracteres no permitidos.');
    }
  };
  // Login


  const envioLogin = async (e) => {
    e.preventDefault();
    //const encrypted = encryptChaCha20(contrasena);
  
    const body = {
      correo,
      contrasena
    };
    console.log('Datos enviados al servidor:', body);
  
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
  
      const data = await response.json();
      if (response.ok) {
        alert('Login exitoso');
      } else {
        alert(data.error || 'Error en login');
      }
    } catch (error) {
      console.error('Error en login:', error);
      alert('Error de conexión con el servidor');
    }
  };

  // Registro
  const CrearLogin = async (e) => {
    e.preventDefault();
    try {
      
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nombre: Nnombre,
          correo: Ncorreo,
          contrasena: Ncontrasena,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert('Usuario creado exitosamente: ' + data.message);
      } else {
        alert('Error al crear usuario: ' + (data.error || 'Intente nuevamente.'));
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error de conexión con el servidor.');

    }
  };

  return (
    <div className="App">
      {/* Login */}
      <h2>Login</h2>
      <form onSubmit={envioLogin}>
        <label>Correo:</label>
        <input type="email" value={correo} onChange={RestriccionCorreo} />
        <label>Contraseña:</label>
        <input type="password" value={contrasena} onChange={RestriccionContrasena} />
        <button type="submit">Iniciar sesión</button>
      </form>

      {/* Registro */}
      <h2>Registro</h2>
      <form onSubmit={CrearLogin}>
        <label>Nombre:</label>
        <input type="text" value={Nnombre} onChange={(e) => setNnombre(e.target.value)} />
        <label>Correo:</label>
        <input type="email" value={Ncorreo} onChange={(e) => setNCorreo(e.target.value)} />
        <label>Contraseña:</label>
        <input type="password" value={Ncontrasena} onChange={(e) => setNContrasena(e.target.value)} />
        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default App;