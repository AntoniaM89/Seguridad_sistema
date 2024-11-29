import React from 'react';

function Inicio({ nombre }) {
  return (
    <div>
      <h1>Bienvenido {nombre}!</h1>
      <p>¡Has iniciado sesión correctamente! Ahora puedes acceder a las funcionalidades de la aplicación.</p>
    </div>
  );
}

export default Inicio;