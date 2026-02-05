import React, { useState } from 'react';
import '../App.css';
import axios from "axios";
import { API_ENDPOINTS } from '../config/api';
import Modal from './Modal';
import PantallaCarga from './PantallaCarga';

function InstruccionesSilabas({ alClickCasa, alClickRegresar, alClickJugarSilabas, numImagenes = 3 }) {
    const [cargando, setCargando] = useState(false);
    const [mostrarError, setMostrarError] = useState(false);
    const [mensajeError, setMensajeError] = useState('');

    const iniciarJuegoSilabas = async () => {
        setCargando(true);
        try {
            const res = await axios.get(`${API_ENDPOINTS.SILABAS}?cantidad=${numImagenes}`);
            alClickJugarSilabas(res.data);
        } catch (err) {
            console.error("Error al obtener datos:", err);

            // Determinar mensaje de error específico
            if (err.response) {
                setMensajeError(`Error del servidor (${err.response.status}). Por favor, intenta de nuevo.`);
            } else if (err.request) {
                setMensajeError("No se pudo conectar con el servidor. Verifica tu conexión a internet.");
            } else {
                setMensajeError("Error al cargar el juego. Intenta de nuevo.");
            }

            setMostrarError(true);
        } finally {
            setCargando(false);
        }
    };

    // Mostrar pantalla de carga mientras se obtienen las palabras
    if (cargando) {
        return <PantallaCarga mensaje="Preparando sílabas..." />;
    }

    return (
        <div id="syllables-instructions-screen" className="screen">{/* ...existing code... */}
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>
            <button className="regresar-btn top-left_2 game-card-btn" onClick={alClickRegresar} aria-label="Regresar a selección de modos">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="m12 19-7-7 7-7"/>
                    <path d="M19 12H5"/>
                </svg>
            </button>
            <div className="content-center">
                <h1 className="title" tabIndex="0">Como jugar?</h1>
                <div className="instruction-card">
                    <p className="instruction-text" tabIndex="0">1. Se te mostrara una imagen y una palabra incompleta.</p>
                    <p className="instruction-text" tabIndex="0">2. Tu tarea es elegir la silaba correcta que falta para completar la palabra.</p>
                    <p className="instruction-text" tabIndex="0">
                        3. Responderás {numImagenes} {numImagenes === 1 ? 'palabra' : 'palabras'} en total.
                    </p>
                </div>
                <button
                    className="btn-primary"
                    onClick={iniciarJuegoSilabas}
                    aria-label="Empezar juego de sílabas"
                >
                    Empezar
                </button>
            </div>

            {/* Modal de error */}
            <Modal
                mostrar={mostrarError}
                onCerrar={() => setMostrarError(false)}
                titulo="Error al cargar"
                mensaje={mensajeError}
                tipo="error"
                textoBoton="OK"
            />
        </div>
    );
}

export default InstruccionesSilabas;
