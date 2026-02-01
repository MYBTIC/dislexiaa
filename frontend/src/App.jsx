import React, {useState, useEffect} from 'react';
import Inicio from './components/Inicio';
import SeleccionModos from './components/SeleccionModos';
import ModoAnagrama from './components/ModoAnagrama';
import ModoSilabas from './components/ModoSilabas';
import InstruccionesAnagrama from "./components/InstruccionesAnagrama";
import InstruccionesSilabas from "./components/InstruccionesSilabaCorrecta.jsx";
import Oración from "./components/Oración";
// Importa las demás según las necesites
import './App.css';


function App() {

    // Estado para controlar qué pantalla ver (home por defecto)
    const [pantallaActiva, setPantallaActiva] = useState('home');

    // ESTADO GLOBAL: Vive aquí para que no se pierda
    const [listaPalabras, setListaPalabras] = useState([]);
    const [indiceActual, setIndiceActual] = useState(0);
    const [modoActual, setModoActual] = useState(''); // 'anagrama' o 'silabas'

    // 1. FUNCIÓN PARA LIMPIAR TODO AL REGRESAR
    const regresarHome = () => {
        setIndiceActual(0);      // Reseteamos el progreso
        setPantallaActiva('home'); // Volvemos al inicio
    };

    const iniciarJuegoAnagrama = (datosRecibidos) => {
        setListaPalabras(datosRecibidos);
        setModoActual('anagrama');
        setPantallaActiva('jugarAnagrama');
    };

    // NUEVA FUNCIÓN PARA SÍLABAS
    const iniciarJuegoSilabas = (datosRecibidos) => {
        setListaPalabras(datosRecibidos);
        setModoActual('silabas');
        setPantallaActiva('jugarSilabas');
    };

    const siguientePalabraAnagrama = (nuevoIndice) => {
        setIndiceActual(nuevoIndice);
        setPantallaActiva('jugarAnagrama');
    };

    const siguientePalabraSilabas = (nuevoIndice) => {
        setIndiceActual(nuevoIndice);
        setPantallaActiva('jugarSilabas');
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
                    alSeleccionarSilabas={() => setPantallaActiva('silabas')}
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

            {/* NUEVA PANTALLA DE INSTRUCCIONES SÍLABAS */}
            {pantallaActiva === 'silabas' && (
                <InstruccionesSilabas
                    alClickJugarSilabas={iniciarJuegoSilabas}
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

            {pantallaActiva === 'jugarSilabas' && (
                <ModoSilabas
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
                    alClickJugarAnagrama={modoActual === 'anagrama' ? siguientePalabraAnagrama : siguientePalabraSilabas}
                />
            )}
        </div>
    );
}

export default App;