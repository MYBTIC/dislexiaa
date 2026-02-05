import React, { useState, useEffect } from 'react';
import '../App.css';
import './PantallaError.css';

function PantallaError({ alClickCasa, alContinuar, respuestaCorrecta, tipoJuego, intentos, maxIntentos = 3 }) {
    const [mostrarContador, setMostrarContador] = useState(true);
    const intentosRestantes = maxIntentos - intentos;

    useEffect(() => {
        // Mostrar el contador animado por un momento
        const timer = setTimeout(() => {
            setMostrarContador(false);
        }, 1500);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div id="error-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} aria-label="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <div className="content-center">
                {/* Contador animado de intentos */}
                {mostrarContador && intentosRestantes > 0 && (
                    <div className="contador-intentos-overlay">
                        <div className="contador-circulo spin-animation">
                            <div className="numero-intentos">{intentosRestantes}</div>
                        </div>
                        <p className="texto-intentos">
                            {intentosRestantes === 1 ? '¡Último intento!' : `${intentosRestantes} intentos restantes`}
                        </p>
                    </div>
                )}

                {!mostrarContador && (
                    <div role="alert" aria-live="polite">
                        <div className="error-icon" aria-hidden="true" tabIndex="0">😕</div>
                        <h1 className="title" tabIndex="0">Fallaste</h1>
                        <div className="error-card">
                            <p className="error-text" tabIndex="0">¡Inténtalo de nuevo, tú puedes!</p>
                        </div>
                        <button className="btn-error game-card-btn" onClick={alContinuar} aria-label="Reintentar el ejercicio">
                            Reintentar
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default PantallaError;
