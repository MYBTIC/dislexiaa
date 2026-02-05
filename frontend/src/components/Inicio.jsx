import React from 'react';
import '../App.css';

function Inicio({ alClickJugar, alClickConfig }) {
    return (
        <div id="home-screen" className="screen active">
            {/* Botón de configuración flotante */}
            <button
                className="btn-config-float"
                onClick={alClickConfig}
                aria-label="Configuración"
                title="Configuración"
            >
                ⚙️
            </button>

            <div className="content-center">
                <div className="text-center">
                    <h1 className="title-main" tabIndex="0">Juego de Palabras</h1>
                    <p className="subtitle" tabIndex="0">Aprende jugando con las letras!</p>
                </div>
                <button className="btn-primary btn-large game-card-btn" onClick={alClickJugar} aria-label="Empezar a jugar">
                    Empezar
                </button>
            </div>
        </div>
    );
}

export default Inicio;
