import React, { useEffect } from 'react';
import '../App.css';
import './PantallaIntentosAgotados.css';

/**
 * Pantalla que muestra la respuesta correcta cuando se agotan los intentos
 * Se muestra por 3 segundos y luego continúa automáticamente
 */
function PantallaIntentosAgotados({ palabraActual, alContinuar }) {
    useEffect(() => {
        // Auto continuar después de 3 segundos
        const timer = setTimeout(() => {
            alContinuar();
        }, 3000);

        return () => clearTimeout(timer);
    }, [alContinuar]);

    if (!palabraActual) return null;

    return (
        <div className="pantalla-intentos-agotados" role="alert" aria-live="assertive">
            <div className="contenido-intentos">
                <div className="icono-intentos" aria-hidden="true" tabIndex="0">😊</div>
                <h2 className="titulo-intentos" tabIndex="0">La respuesta correcta es:</h2>

                <div className="tarjeta-respuesta">
                    <img
                        src={palabraActual.imagen}
                        alt={palabraActual.nombre}
                        className="imagen-respuesta"
                    />
                    <p className="palabra-respuesta" tabIndex="0">{palabraActual.nombre}</p>
                </div>

                <div className="mensaje-animo">
                    <p tabIndex="0">¡Sigue intentando, lo estás haciendo muy bien! 💪</p>
                </div>

                {/* Indicador de progreso */}
                <div className="progreso-autoclose">
                    <div className="barra-progreso"></div>
                </div>
            </div>
        </div>
    );
}

export default PantallaIntentosAgotados;
