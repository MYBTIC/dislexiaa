import React from 'react';
import '../App.css';
import { palabrasSilabas } from '../data/datosSilabas';
// import axios from "axios";


function InstruccionesSilabas({ alClickCasa, alClickRegresar, alClickJugarSilabas}) {

    const iniciarJuegoSilabas = () => {
        // Por ahora usamos los datos de prueba en lugar del API
        alClickJugarSilabas(palabrasSilabas);

        // Código comentado para cuando el API esté listo:
        // try {
        //     const res = await axios.get('http://127.0.0.1:8000/api/juego2/');
        //     alClickJugarSilabas(res.data);
        // } catch (err) {
        //     console.error("Error al obtener datos:", err);
        // }
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
                <h1 className="title">¿Cómo jugar? 📝</h1>
                <div className="instruction-card">
                    <p className="instruction-text">1. Se te mostrará una imagen y una palabra incompleta.</p>
                    <p className="instruction-text">2. Tu tarea es elegir la sílaba correcta que falta para completar la palabra.</p>
                    <p className="instruction-text">3. Responderás 10 palabras en total.</p>
                </div>
                <button className="btn-primary" onClick={iniciarJuegoSilabas}>
                    Empezar ▶️
                </button>
            </div>
        </div>
    );
}

export default InstruccionesSilabas;