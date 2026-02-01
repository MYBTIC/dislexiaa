import React, { useEffect, useState } from 'react';
import '../App.css';

export default function PantallaFinal({ alClickCasa, totalPalabras }) {
    const [animacionActiva, setAnimacionActiva] = useState(false);

    useEffect(() => {
        setAnimacionActiva(true);
    }, []);

    return (
        <div className={`pantalla-resultado pantalla-final ${animacionActiva ? 'activa' : ''}`}>
            {/* Confeti de celebración */}
            <div className="confeti-container">
                {[...Array(30)].map((_, i) => (
                    <div key={i} className={`confeti confeti-${i % 5}`} style={{
                        left: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 0.5}s`,
                        animationDuration: `${2 + Math.random() * 2}s`
                    }}></div>
                ))}
            </div>

            <div className="resultado-contenido resultado-final">
                <div className="trofeo-container">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="trofeo-icono">
                        <path d="M6 2h12v6a6 6 0 01-12 0V2z" fill="#fbbf24"/>
                        <path d="M6 2H4a2 2 0 00-2 2v2a4 4 0 004 4" stroke="#f59e0b" strokeWidth="2"/>
                        <path d="M18 2h2a2 2 0 012 2v2a4 4 0 01-4 4" stroke="#f59e0b" strokeWidth="2"/>
                        <path d="M9 22h6" stroke="#d97706" strokeWidth="2" strokeLinecap="round"/>
                        <path d="M12 14v8" stroke="#d97706" strokeWidth="2"/>
                        <circle cx="12" cy="6" r="2" fill="#fef3c7"/>
                    </svg>
                </div>

                <h1 className="titulo-resultado titulo-final">Felicidades!</h1>
                <p className="mensaje-resultado">Has completado todas las palabras</p>

                <div className="estadisticas-final">
                    <div className="stat-item">
                        <span className="stat-numero">{totalPalabras}</span>
                        <span className="stat-label">Palabras completadas</span>
                    </div>
                </div>

                <div className="estrellas-container estrellas-final">
                    <span className="estrella estrella-grande">*</span>
                    <span className="estrella estrella-grande">*</span>
                    <span className="estrella estrella-grande">*</span>
                </div>

                <button className="btn-resultado btn-volver-inicio" onClick={alClickCasa}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                        <polyline points="9 22 9 12 15 12 15 22"/>
                    </svg>
                    <span>Volver al inicio</span>
                </button>
            </div>
        </div>
    );
}
