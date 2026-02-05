import React, { useState } from 'react';
import '../App.css';

function Configuracion({ alClickRegresar, numImagenesActual, alGuardarConfig }) {
    const [numImagenes, setNumImagenes] = useState(numImagenesActual);

    const handleGuardar = () => {
        alGuardarConfig(numImagenes);
        alClickRegresar();
    };

    return (
        <div id="config-screen" className="screen active">
            <div className="content-center">
                {/* Botón de regresar */}
                <button
                    className="btn-back"
                    onClick={alClickRegresar}
                    aria-label="Regresar"
                >
                    ← Volver
                </button>

                <div className="config-container">
                    <div className="config-header">
                        <div className="config-icon">⚙️</div>
                        <h1 className="title-main">Configuración</h1>
                        <p className="subtitle">Personaliza tu experiencia de juego</p>
                    </div>

                    <div className="config-content">
                        <div className="config-section">
                            <label className="config-label">
                                <span className="config-label-icon">🖼️</span>
                                <span className="config-label-text">Número de palabras por juego:</span>
                            </label>

                            <div className="config-number-selector" role="group" aria-label="Selector de número de palabras">
                                <button
                                    className="btn-number-change"
                                    onClick={() => setNumImagenes(Math.max(2, numImagenes - 1))}
                                    disabled={numImagenes <= 2}
                                    aria-label={`Disminuir número de palabras, actual: ${numImagenes}`}
                                >
                                    −
                                </button>

                                <div className="number-display" aria-live="polite">
                                    <span className="number-value">{numImagenes}</span>
                                    <span className="number-label">palabras</span>
                                </div>

                                <button
                                    className="btn-number-change"
                                    onClick={() => setNumImagenes(Math.min(8, numImagenes + 1))}
                                    disabled={numImagenes >= 8}
                                    aria-label={`Aumentar número de palabras, actual: ${numImagenes}`}
                                >
                                    +
                                </button>
                            </div>

                            <div className="config-preview">
                                <p className="config-hint">
                                    {numImagenes === 2 && "⚡ Partidas rápidas - Ideal para principiantes"}
                                    {numImagenes === 3 && "✨ Equilibrado - Recomendado para la mayoría"}
                                    {numImagenes === 4 && "🎯 Intermedio - Buen desafío"}
                                    {numImagenes === 5 && "🌟 Estándar - Duración media"}
                                    {numImagenes >= 6 && "🚀 Desafío largo - Para expertos"}
                                </p>
                            </div>
                        </div>

                        <div className="config-info">
                            <div className="info-card">
                                <span className="info-icon" tabIndex="0">ℹ️</span>
                                <div className="info-text" tabIndex="0">
                                    <strong>Nota:</strong> El cambio se aplicará en la próxima partida
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="config-actions">
                        <button
                            className="btn-secondary btn-large"
                            onClick={alClickRegresar}
                            aria-label="Cancelar cambios y volver"
                        >
                            Cancelar
                        </button>
                        <button
                            className="btn-primary btn-large"
                            onClick={handleGuardar}
                            aria-label="Guardar cambios de configuración"
                        >
                            💾 Guardar Cambios
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Configuracion;
