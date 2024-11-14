
import './App.css';
import { useState } from 'react';

function App() {
  const [correo, setCorreo]= useState("");

  const RestriccionCorreo = (e) => {
      const valor = e.target.value;
      console.log(correo)
      if ((!valor.includes("'")) && (!valor.includes('"')) && !valor.includes('=')){
        setCorreo(valor);
      }
      else{
        alert('Tamos mal perro ctm')
      }
  } 

  const encriptacion = (e) =>

 // https://codesandbox.io/p/devbox/zen-khayyam-zfh775?file=%2Findex.ts
  return (
    <div className="App">
      <form method="post">
        <div>
          <label>correo:</label>
          <input type="email" name="correo" value={correo} onChange={RestriccionCorreo}/>
        </div>
        <div>
          <label>contraseña:</label>
          <input type="password" name="contraseña" />
        </div>
        <button type="submit" value="submit">agregar</button>
      </form>
    </div>
  );
}

export default App;
