import React, {useState, useEffect} from 'react';
import '../App.css';
import PantallaCorrecta from './PantallaCorrecta';
import PantallaError from './PantallaError';

function ModoSilabas({palabras, indice, alClickCasa, alClickOracion}) {
    const [silabaSeleccionada, setSilabaSeleccionada] = useState(null);
    const [mostrarExito, setMostrarExito] = useState(false);
    const [mostrarError, setMostrarError] = useState(false);
    const [intentos, setIntentos] = useState(0);

    useEffect(() => {
        // Resetear la selección cuando cambie la palabra
        setSilabaSeleccionada(null);
        setMostrarExito(false);
        setMostrarError(false);
        setIntentos(0);
    }, [indice]);

    const seleccionarSilaba = (silaba) => {
        setSilabaSeleccionada(silaba);
    };

    const comprobarRespuesta = () => {
        const palabraActual = palabras[indice];
        // La respuesta correcta es la sílaba que está en el índice silaba_oculta
        const respuestaCorrecta = palabraActual.silabas[palabraActual.silaba_oculta];

        if (silabaSeleccionada === respuestaCorrecta) {
            setMostrarExito(true);
        } else {
            setIntentos(intentos + 1);
            setMostrarError(true);
        }
    };

    const continuarDespuesDeExito = () => {
        setMostrarExito(false);
        alClickOracion();
    };

    const continuarDespuesDeError = () => {
        setMostrarError(false);

        // Si ya pasaron 3 intentos, ir a la oración
        if (intentos >= 2) { // Cambiado a 2 para que sean 3 intentos en total
            alClickOracion();
        } else {
            // Resetear la selección para reintentar
            setSilabaSeleccionada(null);
        }
    };

    const reproducirAudio = () => {
        // Usar Web Speech API para reproducir la palabra
        const palabraActual = palabras[indice];
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(palabraActual.nombre);
            utterance.lang = 'es-ES';
            utterance.rate = 0.8; // Velocidad más lenta para niños
            window.speechSynthesis.speak(utterance);
        }
    };

    const palabraActual = palabras[indice];
    if (!palabraActual) return <div className="screen">Cargando juego...</div>;

    // Construir la palabra incompleta (con ___ donde falta la sílaba)
    const construirPalabraIncompleta = () => {
        return palabraActual.silabas.map((silaba, idx) => {
            if (idx === palabraActual.silaba_oculta) {
                return '___';
            }
            return silaba;
        }).join('');
    };

    // La respuesta correcta para mostrar en caso de error
    const respuestaCorrecta = palabraActual.silabas[palabraActual.silaba_oculta];

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
                respuestaCorrecta={respuestaCorrecta}
                tipoJuego="silabas"
                intentos={intentos}
            />
        );
    }

    return (
        <div id="syllables-game-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <button className="audio-btn top-right game-card-btn" onClick={reproducirAudio} aria-label="Reproducir audio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
            </button>

            <div className="progress-counter top-center">
                {indice + 1}/{palabras.length}
            </div>

            <div className="content-center">
                <div className="image-container">
                    <img src={palabraActual.imagen} alt={palabraActual.nombre} className="game-image"/>
                </div>

                <div className="game-card-white">
                    <h2 className="word-display">{construirPalabraIncompleta()}</h2>

                    <div className="syllables-options">
                        {palabraActual.opciones.map((silaba, index) => (
                            <div
                                key={index}
                                className={`syllable-option ${silabaSeleccionada === silaba ? 'selected' : ''}`}
                                onClick={() => seleccionarSilaba(silaba)}
                                tabIndex="0"
                                role="button"
                                aria-label={`Opción ${silaba}`}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' || e.key === ' ') {
                                        e.preventDefault();
                                        seleccionarSilaba(silaba);
                                    }
                                }}
                            >
                                {silaba}
                            </div>
                        ))}
                    </div>

                    {silabaSeleccionada && (
                        <div id="check-button-container">
                            <button className="btn-check game-card-btn" onClick={comprobarRespuesta}>
                                Comprobar
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ModoSilabas;
