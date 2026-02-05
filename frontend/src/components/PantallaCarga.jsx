import React from 'react';
import './PantallaCarga.css';

function PantallaCarga({ mensaje = "Preparando el juego..." }) {
    return (
        <div className="pantalla-carga-overlay">
            <div className="pantalla-carga-contenido">
                <div className="spinner-container">
                    <div className="spinner"></div>
                    <div className="spinner-glow"></div>
                </div>
                <h2 className="loading-title" tabIndex="0">{mensaje}</h2>
                <div className="loading-dots">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                </div>
            </div>
        </div>
    );
}

export default PantallaCarga;
