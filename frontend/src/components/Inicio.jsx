import React from 'react';
import '../App.css';

function Inicio({ alClickJugar }) {
    return (
        <div id="home-screen" className="screen active">
            <div className="content-center">
                <div className="text-center">
                    <h1 className="title-main">Juego de Palabras</h1>
                    <p className="subtitle">Aprende jugando con las letras!</p>
                </div>
                <button className="btn-primary btn-large game-card-btn" onClick={alClickJugar}>
                    Empezar
                </button>
            </div>
        </div>
    );
}

export default Inicio;
