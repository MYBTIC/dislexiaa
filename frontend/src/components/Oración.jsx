import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../App.css';

function Oracion({palabras, indice, alClickCasa, alClickJugarAnagrama}) {
    const [oracion, setOracion] = useState("");
    const [cargando, setCargando] = useState(false); // Estado para controlar la carga
    const [textoReconocido, setTextoReconocido] = useState("Presiona el micro y repite la oración...");

    const palabraActual = palabras[indice];

    useEffect(() => {
        const obtenerOracion = async () => {
            if (palabraActual) {
                setOracion(""); // Limpiamos la oración anterior inmediatamente
                setCargando(true); // Iniciamos la animación de carga
                try {
                    const res = await axios.post('http://127.0.0.1:8000/api/oracion/', {
                        palabra: palabraActual.nombre
                    });
                    setOracion(res.data.oracion);
                } catch (err) {
                    console.error("Error con Gemini:", err);
                    setOracion(`Mira la ${palabraActual.nombre} que está en la mesa.`);
                } finally {
                    setCargando(false); // Finalizamos la carga
                }
            }
        };

        obtenerOracion();
    }, [palabraActual]);

    // Uso de micrófono
    const activarMicrofono = () => {
        // 1. Verificamos si el navegador soporta el reconocimiento de voz
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!Recognition) {
            alert("Tu navegador no soporta reconocimiento de voz. Prueba con Google Chrome.");
            return;
        }

        const recognition = new Recognition();
        recognition.lang = 'es-ES'; // Idioma español
        recognition.interimResults = false; // Solo muestra el resultado final
        recognition.continuous = false; // Se detiene al terminar de hablar

        // Evento que se dispara cuando el micro empieza a escuchar
        recognition.onstart = () => {
            setTextoReconocido("Escuchando... 🎙️");
        };

        // Evento que captura el resultado de la voz
        recognition.onresult = (event) => {
            const vozCapturada = event.results[0][0].transcript;

            // Aplicamos el formato de Mayúscula y Punto
            const textoConFormato = formatearTexto(vozCapturada);

            // Guardamos el resultado final formateado
            setTextoReconocido(textoConFormato);
        };

        // Evento por si ocurre un error (silencio prolongado o bloqueo de micro)
        recognition.onerror = (event) => {
            console.error("Error de micro:", event.error);
            setTextoReconocido("No se pudo escuchar nada, intenta de nuevo.");
        };

        recognition.start(); // Inicia el proceso de escucha
    };

    const formatearTexto = (texto) => {
        if (!texto) return "";
        let t = texto.trim();
        // Poner mayúscula inicial
        t = t.charAt(0).toUpperCase() + t.slice(1);
        // Añadir punto final si no tiene
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
            alert("¡Felicidades! Completaste todas las palabras. 🎉");
            alClickCasa();
        }
    };

    const validarOracion = () =>{
        if (oracion === textoReconocido){
            controlarFinJuego();
        } else{
            alert("¡Oh no! La oración no es igual. Intenta leerla de nuevo exactamente como aparece. 💪");
        }
    };

    if (!palabraActual) return <div className="screen">Cargando juego...</div>;

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
                                    <span className="loading-text">Se está creando tu oración... ✨</span>
                                ) : (
                                    renderizarOracion(oracion, palabraActual.nombre)
                                )}
                            </h2>
                        </div>

                        <div className="transcript-display">
                            <p className="text-placeholder">
                                {textoReconocido}
                            </p>
                        </div>

                        <div className="actions-row">
                            <button className="btn-mic game-card-btn" onClick={activarMicrofono}>
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