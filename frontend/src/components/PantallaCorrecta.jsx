import React, { useEffect } from 'react';
import '../App.css';

function PantallaCorrecta({ alContinuar }) {
    // Auto continuar después de 2 segundos
    useEffect(() => {
        const timer = setTimeout(() => {
            alContinuar();
        }, 2000);

        return () => clearTimeout(timer);
    }, [alContinuar]);

    return (
        <div className="screen success-overlay" role="alert" aria-live="assertive">
            <div className="content-center">
                <div className="success-icon" aria-hidden="true" tabIndex="0">🎉</div>
                <h1 className="title success-title" tabIndex="0">¡Correcto!</h1>
                <div className="success-card">
                    <p className="success-text" tabIndex="0">¡Excelente trabajo!</p>
                </div>
            </div>
        </div>
    );
}

export default PantallaCorrecta;
