import React, {useState, useEffect} from 'react';
import '../App.css';
import PantallaCorrecta from './PantallaCorrecta';
import PantallaError from './PantallaError';

function ModoAnagrama({palabras, indice, alClickCasa, alClickOracion}) {
    const [letrasDisponibles, setLetrasDisponibles] = useState([]);
    const [letrasSeleccionadas, setLetrasSeleccionadas] = useState([]);
    const [mostrarExito, setMostrarExito] = useState(false);
    const [mostrarError, setMostrarError] = useState(false);

    useEffect(() => {
        if (palabras && palabras[indice]) {
            prepararRonda(palabras[indice]);
        }
    }, [palabras, indice]);

    const prepararRonda = (palabraData) => {
        if (!palabraData) return;
        setLetrasSeleccionadas([]);
        setMostrarExito(false);
        setMostrarError(false);
        let letras = palabraData.palabra_dividida_letras
            .split('-')
            .sort(() => Math.random() - 0.5);
        setLetrasDisponibles(letras);
    };

    const seleccionarLetra = (letra, index) => {
        setLetrasSeleccionadas([...letrasSeleccionadas, letra]);
        setLetrasDisponibles(letrasDisponibles.filter((_, i) => i !== index));
    };

    const quitarLetra = (letra, index) => {
        setLetrasDisponibles([...letrasDisponibles, letra]);
        setLetrasSeleccionadas(letrasSeleccionadas.filter((_, i) => i !== index));
    };

    const comprobarRespuesta = () => {
        const preguntaActual = palabras[indice];
        const respuestaJugador = letrasSeleccionadas.join('');

        if (respuestaJugador === preguntaActual.nombre) {
            setMostrarExito(true);
        } else {
            setMostrarError(true);
        }
    };

    const continuarDespuesDeExito = () => {
        setMostrarExito(false);
        alClickOracion();
    };

    const continuarDespuesDeError = () => {
        setMostrarError(false);
        alClickOracion();
    };

    // Función auxiliar para activar letras con Enter o Espacio
    const manejarTeclaLetra = (e, callback) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            callback();
        }
    };

    // Lógica global de teclado (para escritura directa)
    useEffect(() => {
        const manejarEscrituraDirecta = (event) => {
            const tecla = event.key.toUpperCase();
            if (event.key === "Backspace" && letrasSeleccionadas.length > 0) {
                const ultimoIndice = letrasSeleccionadas.length - 1;
                quitarLetra(letrasSeleccionadas[ultimoIndice], ultimoIndice);
            }
            if (event.key === "Enter" && letrasSeleccionadas.length === palabras[indice].nombre.length) {
                comprobarRespuesta();
            }
            const indexDisponible = letrasDisponibles.findIndex(l => l.toUpperCase() === tecla);
            if (indexDisponible !== -1) {
                seleccionarLetra(letrasDisponibles[indexDisponible], indexDisponible);
            }
        };

        window.addEventListener('keydown', manejarEscrituraDirecta);
        return () => window.removeEventListener('keydown', manejarEscrituraDirecta);
    }, [letrasDisponibles, letrasSeleccionadas, palabras, indice]);

    const palabraActual = palabras[indice];
    if (!palabraActual) return <div className="screen">Cargando juego...</div>;

    // Mostrar pantalla de éxito
    if (mostrarExito) {
        return <PantallaCorrecta alContinuar={continuarDespuesDeExito} />;
    }

    // Mostrar pantalla de error
    if (mostrarError) {
        return (
            <PantallaError
                alClickCasa={alClickCasa}
                alContinuar={continuarDespuesDeError}
                respuestaCorrecta={palabraActual.nombre}
                tipoJuego="anagrama"
            />
        );
    }

    return (
        <div id="anagram-game-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <div className="progress-counter top-center">
                {indice + 1}/{palabras.length}
            </div>

            <div className="content-center">
                <div className="image-container">
                    <img src={palabraActual.imagen} alt="Referencia visual" className="game-image"/>
                </div>

                <div className="game-card-white">
                    {/* Letras ya elegidas (se pueden quitar con TAB + Enter) */}
                    <div className="letters-selected">
                        {letrasSeleccionadas.map((letra, i) => (
                            <div
                                key={i}
                                className="letter-slot"
                                onClick={() => quitarLetra(letra, i)}
                                onKeyDown={(e) => manejarTeclaLetra(e, () => quitarLetra(letra, i))}
                                tabIndex="0"
                                role="button"
                                aria-label={`Quitar letra ${letra}`}
                            >
                                {letra}
                            </div>
                        ))}
                        {Array(palabraActual.nombre.length - letrasSeleccionadas.length).fill(0).map((_, i) => (
                            <div key={i} className="empty-slot"></div>
                        ))}
                    </div>

                    {/* Letras para elegir (se seleccionan con TAB + Enter) */}
                    <div className="letters-available">
                        {letrasDisponibles.map((letra, i) => (
                            <div
                                key={i}
                                className="letter-available"
                                onClick={() => seleccionarLetra(letra, i)}
                                onKeyDown={(e) => manejarTeclaLetra(e, () => seleccionarLetra(letra, i))}
                                tabIndex="0"
                                role="button"
                                aria-label={`Seleccionar letra ${letra}`}
                            >
                                {letra}
                            </div>
                        ))}
                    </div>

                    {letrasSeleccionadas.length === palabraActual.nombre.length && (
                        <div id="check-button-container">
                            <button className="btn-check game-card-btn" onClick={comprobarRespuesta}>Comprobar</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ModoAnagrama;