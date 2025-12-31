import React, {useState} from 'react';
import Inicio from './components/Inicio';
import SeleccionModos from './components/SeleccionModos';
import ModoAnagrama from './components/ModoAnagrama';
import InstruccionesAnagrama from "./components/InstruccionesAnagrama";
import Oración from "./components/Oración";
// Importa las demás según las necesites
import './App.css';


function App() {
    // Estado para controlar qué pantalla ver (home por defecto)
    const [pantallaActiva, setPantallaActiva] = useState('anagrama');

    // ESTADO GLOBAL: Vive aquí para que no se pierda
    const [listaPalabras, setListaPalabras] = useState([]);
    const [indiceActual, setIndiceActual] = useState(0);

    // 1. FUNCIÓN PARA LIMPIAR TODO AL REGRESAR
    const regresarHome = () => {
        setIndiceActual(0);      // Reseteamos el progreso
        setPantallaActiva('home'); // Volvemos al inicio
    };

    const iniciarJuegoAnagrama = (datosRecibidos) => {
        setListaPalabras(datosRecibidos); // Aquí se guardan los datos que enviaste desde el hijo
        setPantallaActiva('jugarAnagrama');      // Cambias la pantalla para empezar a jugar
    };

    const siguientePalabraAnagrama = (nuevoIndice) => {
        setIndiceActual(nuevoIndice); // Aquí se guardan los datos que enviaste desde el hijo
        setPantallaActiva('jugarAnagrama');      // Cambias la pantalla para empezar a jugar
    };

    return (
        <div className="App">
            {/* Lógica de navegación condicional */}

            {pantallaActiva === 'home' && (
                <Inicio alClickJugar={() => setPantallaActiva('seleccion')}/>
            )}

            {pantallaActiva === 'seleccion' && (
                <SeleccionModos
                    alSeleccionarAnagrama={() => setPantallaActiva('anagrama')}
                    alClickRegresar={() => setPantallaActiva('home')}
                    alClickCasa={regresarHome}
                />
            )}

            {pantallaActiva === 'anagrama' && (
                <InstruccionesAnagrama
                    alClickJugarAnagrama={iniciarJuegoAnagrama}
                    alClickRegresar={() => setPantallaActiva('seleccion')}
                    alClickCasa={regresarHome}
                />
            )}

            {pantallaActiva === 'jugarAnagrama' && (
                <ModoAnagrama
                    palabras={listaPalabras}
                    indice={indiceActual}
                    alClickCasa={regresarHome}
                    alClickOracion={() => setPantallaActiva('oracion')}
                />
            )}

            {pantallaActiva === 'oracion' && (
                <Oración
                    palabras={listaPalabras}
                    indice={indiceActual}
                    alClickCasa={regresarHome}
                    alClickJugarAnagrama={siguientePalabraAnagrama}
                />
            )}

            {/* Agrega aquí las pantallas de instrucciones o errores después */}
        </div>
    );
}

export default App;