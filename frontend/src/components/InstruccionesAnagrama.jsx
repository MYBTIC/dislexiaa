import React, { useState } from 'react';
import '../App.css';
import axios from "axios";

function InstruccionesAnagrama({ alClickJugarAnagrama, alClickCasa, alClickRegresar }) {
    const [cargando, setCargando] = useState(false);

    const iniciarJuegoAnagrama = async () => {
        setCargando(true);
        try {
            const res = await axios.get('http://127.0.0.1:8000/api/juego1/');
            alClickJugarAnagrama(res.data);
        } catch (err) {
            console.error("Error al obtener datos:", err);
            // Si falla, intentar de nuevo o mostrar error
            alert("Error al cargar el juego. Intenta de nuevo.");
        } finally {
            setCargando(false);
        }
    };

    return (
        <div id="anagram-instructions-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>
            <button className="regresar-btn top-left_2 game-card-btn" onClick={alClickRegresar}>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m12 19-7-7 7-7"/>
                    <path d="M19 12H5"/>
                </svg>
            </button>
            <div className="content-center">
                <h1 className="title">Como jugar?</h1>
                <div className="instruction-card">
                    <p className="instruction-text">1. Mira la imagen y las letras desordenadas.</p>
                    <p className="instruction-text">2. Ordena las letras para formar la palabra correcta.</p>
                    <p className="instruction-text">3. Lee la oracion especial que aparecera al terminar!</p>
                </div>
                <button
                    className="btn-primary"
                    onClick={iniciarJuegoAnagrama}
                    disabled={cargando}
                >
                    {cargando ? (
                        <span className="loading-spinner">Cargando palabras...</span>
                    ) : (
                        "Empezar"
                    )}
                </button>
            </div>
        </div>
    );
}

export default InstruccionesAnagrama;
