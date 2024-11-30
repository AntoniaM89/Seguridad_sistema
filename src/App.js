import './App.css';
import { useEffect, useState } from 'react';
import sha256 from "js-sha256";
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';

function App() {
  const [correo, setCorreo] = useState(""); 
  const [contrasena, setContrasena] = useState(""); 
  const [Ncorreo, setNCorreo] = useState(""); 
  const [Ncontrasena, setNContrasena] = useState(""); 
  const [Nnombre, setNnombre] = useState(""); 
  const [loggedIn, setLoggedIn] = useState(false); 
  const [nombre, setNombre] = useState(""); 

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

  useEffect(() => {
    // Verificar si hay una sesión activa
    const sessionId = Cookies.get('session_id');
    if (sessionId) {
      setLoggedIn(true);
    }
  }, []);

  const envioLogin = async (e) => {
    e.preventDefault();
    const Lcontrasena = sha256(contrasena).toUpperCase();
    const Lcorreo = sha256(correo).toUpperCase();
    const body = { Lcorreo, Lcontrasena };

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include', // Para recibir cookies desde el backend
      });

      const data = await response.json();

      if (response.ok) {
        setNombre(data.nombre);
        setLoggedIn(true);
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
    const CorreoSN = Ncorreo;
    const NNcontrasena = sha256(Ncontrasena).toUpperCase();
    const NNcorreo = sha256(Ncorreo).toUpperCase();
    const body = {
      Nnombre,
      CorreoSN,
      NNcorreo,
      NNcontrasena
    };
    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
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
    <Router>
      <div className="App">
        {/* Rutas */}
        <Routes>
          {/* Ruta de login */}
          <Route 
            path="/login" 
            element={loggedIn ? <Navigate to="/" /> : (
              <div>
                <h2>Login</h2>
                <form onSubmit={envioLogin}>
                  <label>Correo:</label>
                  <input type="email" value={correo} onChange={RestriccionCorreo} />
                  <label>Contraseña:</label>
                  <input type="password" value={contrasena} onChange={RestriccionContrasena} />
                  <button type="submit">Iniciar sesión</button>
                </form>

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
            )} 
          />
          
          {/* Ruta de bienvenida que muestra el nombre del usuario si está logueado */}
          <Route 
            path="/" 
            element={loggedIn ? <Bienvenida nombre={nombre} /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

// Componente de bienvenida
function Bienvenida({ nombre }) {
  return (
    <div>
      <h1>Bienvenido, {nombre}!</h1>
      <p>Has iniciado sesión correctamente. ¡Disfruta de la aplicación!</p>
    </div>
  );
}

export default App;
