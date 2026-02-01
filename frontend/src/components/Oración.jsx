import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';
import PantallaReintentar from './PantallaReintentar';
import PantallaFinal from './PantallaFinal';

function Oracion({ palabras, indice, alClickCasa, alClickJugarAnagrama }) {
    const [oracion, setOracion] = useState("");
    const [cargando, setCargando] = useState(false);
    const [textoReconocido, setTextoReconocido] = useState("Presiona el microfono y repite la oracion...");
    const [mostrarReintentar, setMostrarReintentar] = useState(false);
    const [mostrarFinal, setMostrarFinal] = useState(false);
    const [escuchando, setEscuchando] = useState(false);

    const palabraActual = palabras[indice];

    useEffect(() => {
        const obtenerOracion = async () => {
            if (palabraActual) {
                setOracion("");
                setCargando(true);
                setTextoReconocido("Presiona el microfono y repite la oracion...");
                try {
                    const res = await axios.post('http://127.0.0.1:8000/api/oracion/', {
                        palabra: palabraActual.nombre
                    });
                    setOracion(res.data.oracion);
                } catch (err) {
                    console.error("Error con Gemini:", err);
                    setOracion(`Mira el ${palabraActual.nombre} que esta en la mesa`);
                } finally {
                    setCargando(false);
                }
            }
        };

        obtenerOracion();
    }, [palabraActual]);

    // Uso de micrófono
    const activarMicrofono = () => {
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!Recognition) {
            alert("Tu navegador no soporta reconocimiento de voz. Prueba con Google Chrome.");
            return;
        }

        const recognition = new Recognition();
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.continuous = false;

        recognition.onstart = () => {
            setEscuchando(true);
            setTextoReconocido("Escuchando...");
        };

        recognition.onresult = (event) => {
            const vozCapturada = event.results[0][0].transcript;
            const textoConFormato = formatearTexto(vozCapturada);
            setTextoReconocido(textoConFormato);
            setEscuchando(false);
        };

        recognition.onerror = (event) => {
            console.error("Error de micro:", event.error);
            setTextoReconocido("No se pudo escuchar nada, intenta de nuevo.");
            setEscuchando(false);
        };

        recognition.onend = () => {
            setEscuchando(false);
        };

        recognition.start();
    };

    const formatearTexto = (texto) => {
        if (!texto) return "";
        let t = texto.trim();
        t = t.charAt(0).toUpperCase() + t.slice(1);
        if (!t.endsWith('.')) {
            t += '.';
        }
        return t;
    };

    // Función para resaltar la palabra clave
    const renderizarOracion = (texto, palabraClave) => {
        if (!texto) return "";
        const partes = texto.split(new RegExp(`(${palabraClave})`, 'gi'));
        return partes.map((parte, i) =>
            parte.toLowerCase() === palabraClave.toLowerCase()
                ? <span key={i} className="highlight-word">{parte}</span>
                : parte
        );
    };

    const controlarFinJuego = () => {
        if (indice < palabras.length - 1) {
            alClickJugarAnagrama(indice + 1);
        } else {
            setMostrarFinal(true);
        }
    };

    const validarOracion = () => {
        // Normalizar ambas cadenas para comparación más flexible
        const normalizar = (str) => str.toLowerCase().replace(/[.,!?]/g, '').trim();

        if (normalizar(oracion) === normalizar(textoReconocido)) {
            controlarFinJuego();
        } else {
            setMostrarReintentar(true);
        }
    };

    const intentarDeNuevo = () => {
        setMostrarReintentar(false);
        setTextoReconocido("Presiona el microfono y repite la oracion...");
    };

    if (!palabraActual) return <div className="screen">Cargando juego...</div>;

    // Mostrar pantalla final
    if (mostrarFinal) {
        return <PantallaFinal alClickCasa={alClickCasa} totalPalabras={palabras.length} />;
    }

    // Mostrar pantalla de reintentar
    if (mostrarReintentar) {
        return <PantallaReintentar alClickCasa={alClickCasa} alIntentarDeNuevo={intentarDeNuevo} />;
    }

    return (
        <div id="anagram-game-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <div className="progress-counter top-center">
                {indice + 1}/{palabras.length}
            </div>

            <div className="game-main-container">
                <div className="left-panel-small">
                    <div className="image-container-v2">
                        <img src={palabraActual.imagen} alt="Juego" className="game-image-v2"/>
                    </div>
                    <h1 className="word-title">{palabraActual.nombre}</h1>
                </div>

                <div className="right-panel-large">
                    <div className="sentence-layout">
                        <div className="sentence-header">
                            <h2 className="main-sentence">
                                {cargando ? (
                                    <span className="loading-text">Se esta creando tu oracion...</span>
                                ) : (
                                    renderizarOracion(oracion, palabraActual.nombre)
                                )}
                            </h2>
                        </div>

                        <div className="transcript-display">
                            <p className={`text-placeholder ${textoReconocido.includes('Escuchando') ? 'text-active' : ''}`}>
                                {textoReconocido}
                            </p>
                        </div>

                        <div className="actions-row">
                            <button
                                className={`btn-mic game-card-btn ${escuchando ? 'mic-activo' : ''}`}
                                onClick={activarMicrofono}
                                disabled={escuchando}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
                                     fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                                     strokeLinejoin="round">
                                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
                                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                                    <line x1="12" x2="12" y1="19" y2="22"></line>
                                </svg>
                            </button>

                            <button className="btn-continue game-card-btn" onClick={validarOracion} disabled={cargando}>
                                <span>Continuar</span>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                     fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                                     strokeLinejoin="round">
                                    <path d="m9 18 6-6-6-6"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Oracion;
