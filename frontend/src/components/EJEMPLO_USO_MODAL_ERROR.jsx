/* ========================================
   EJEMPLO: Cómo usar el Modal para el error
   "Error al cargar el juego. Intenta de nuevo."
   ======================================== */

import React, { useState } from 'react';
import Modal from './Modal';
import axios from 'axios';
import API_URL from '../config/api';

const SeleccionModos = ({ iniciarJuegoAnagrama, iniciarJuegoSilabas, numImagenes }) => {
    // Estado para controlar el modal de error
    const [mostrarError, setMostrarError] = useState(false);
    const [mensajeError, setMensajeError] = useState('');

    // Función para cargar el juego de Anagramas
    const cargarJuegoAnagrama = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/juego1/?cantidad=${numImagenes}`);
            
            if (response.data && response.data.length > 0) {
                iniciarJuegoAnagrama(response.data);
            } else {
                setMensajeError("No se encontraron palabras para el juego.");
                setMostrarError(true);
            }
        } catch (error) {
            console.error("Error al cargar el juego:", error);
            
            // Determinar el mensaje de error apropiado
            if (error.response) {
                // Error del servidor (4xx, 5xx)
                setMensajeError(`Error del servidor: ${error.response.status}. Intenta de nuevo.`);
            } else if (error.request) {
                // No hay respuesta del servidor
                setMensajeError("No se pudo conectar con el servidor. Verifica tu conexión.");
            } else {
                // Error en la configuración de la petición
                setMensajeError("Error al cargar el juego. Intenta de nuevo.");
            }
            
            setMostrarError(true);
        }
    };

    // Función para cargar el juego de Sílabas
    const cargarJuegoSilabas = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/juego2/?cantidad=${numImagenes}`);
            
            if (response.data && response.data.length > 0) {
                iniciarJuegoSilabas(response.data);
            } else {
                setMensajeError("No se encontraron palabras para el juego de sílabas.");
                setMostrarError(true);
            }
        } catch (error) {
            console.error("Error al cargar el juego de sílabas:", error);
            
            if (error.response) {
                setMensajeError(`Error del servidor: ${error.response.status}. Intenta de nuevo.`);
            } else if (error.request) {
                setMensajeError("No se pudo conectar con el servidor. Verifica tu conexión.");
            } else {
                setMensajeError("Error al cargar el juego. Intenta de nuevo.");
            }
            
            setMostrarError(true);
        }
    };

    return (
        <div className="seleccion-modos">
            <h1 tabIndex="0">Selecciona un Modo de Juego</h1>

            <div className="botones-modos">
                <button onClick={cargarJuegoAnagrama}>
                    🔤 Modo Anagrama
                </button>
                
                <button onClick={cargarJuegoSilabas}>
                    📝 Modo Sílabas
                </button>
            </div>

            {/* Modal de Error - Reemplaza el alert("localhost:5173 says") */}
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
};

export default SeleccionModos;

/* ========================================
   MEJORAS ADICIONALES
   ======================================== */

// También puedes agregar un modal de carga mientras esperas la respuesta:

const SeleccionModosConCarga = ({ iniciarJuegoAnagrama, numImagenes }) => {
    const [mostrarError, setMostrarError] = useState(false);
    const [mensajeError, setMensajeError] = useState('');
    const [cargando, setCargando] = useState(false);

    const cargarJuegoAnagrama = async () => {
        setCargando(true); // Mostrar indicador de carga
        
        try {
            const response = await axios.get(`${API_URL}/api/juego1/?cantidad=${numImagenes}`);
            iniciarJuegoAnagrama(response.data);
        } catch (error) {
            setMensajeError("Error al cargar el juego. Intenta de nuevo.");
            setMostrarError(true);
        } finally {
            setCargando(false); // Ocultar indicador de carga
        }
    };

    return (
        <div>
            <button onClick={cargarJuegoAnagrama} disabled={cargando}>
                {cargando ? "Cargando..." : "🔤 Modo Anagrama"}
            </button>

            <Modal
                mostrar={mostrarError}
                onCerrar={() => setMostrarError(false)}
                titulo="Error"
                mensaje={mensajeError}
                tipo="error"
            />
        </div>
    );
};
