import React, { useState } from 'react';
import '../App.css';
import axios from "axios";

function InstruccionesSilabas({ alClickCasa, alClickRegresar, alClickJugarSilabas }) {
    const [cargando, setCargando] = useState(false);

    const iniciarJuegoSilabas = async () => {
        setCargando(true);
        try {
            const res = await axios.get('http://127.0.0.1:8000/api/juego2/');
            alClickJugarSilabas(res.data);
        } catch (err) {
            console.error("Error al obtener datos:", err);
            alert("Error al cargar el juego. Intenta de nuevo.");
        } finally {
            setCargando(false);
        }
    };

    return (
        <div id="syllables-instructions-screen" className="screen">
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
                    <p className="instruction-text">1. Se te mostrara una imagen y una palabra incompleta.</p>
                    <p className="instruction-text">2. Tu tarea es elegir la silaba correcta que falta para completar la palabra.</p>
                    <p className="instruction-text">3. Responderas 5 palabras en total.</p>
                </div>
                <button
                    className="btn-primary"
                    onClick={iniciarJuegoSilabas}
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

export default InstruccionesSilabas;
