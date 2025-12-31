import React from 'react';
import '../App.css';

function SeleccionModos({ alSeleccionarAnagrama, alClickCasa, alClickRegresar }) {

    // Función para manejar la tecla Enter o Espacio
    const manejarTeclado = (e, accion) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault(); // Evita el scroll con la tecla espacio
            accion();
        }
    };

    return (
        <div id="selection-screen" className="screen">
            <button className="home-btn top-left game-card-btn" onClick={alClickCasa} title="Ir al inicio">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </button>

            <button className="regresar-btn top-left_2 game-card-btn" onClick={alClickRegresar} title="Regresar">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="m12 19-7-7 7-7"/>
                    <path d="M19 12H5"/>
                </svg>
            </button>

            <div className="content-center">
                <h1 className="title">Elige el juego</h1>
                <div className="game-grid">

                    {/* Tarjeta Anagrama */}
                    <div
                        className="game-card"
                        onClick={alSeleccionarAnagrama}
                        onKeyDown={(e) => manejarTeclado(e, alSeleccionarAnagrama)}
                        tabIndex="0"           // Hace que el div sea enfocable con TAB
                        role="button"          // Indica a lectores de pantalla que actúa como botón
                        aria-label="Jugar Anagrama"
                    >
                        <div className="game-icon">🔤</div>
                        <h2 className="game-title">Anagrama</h2>
                        <p className="game-description">Ordena las letras para formar la palabra correcta</p>
                    </div>

                    {/* Tarjeta Sílabas */}
                    <div
                        className="game-card"
                        onKeyDown={(e) => manejarTeclado(e, () => alert("Próximamente"))}
                        tabIndex="0"
                        role="button"
                        aria-label="Jugar Sílabas correctas"
                    >
                        <div className="game-icon">📝</div>
                        <h2 className="game-title">Sílabas correctas</h2>
                        <p className="game-description">Encuentra la sílaba que falta en cada palabra</p>
                    </div>

                </div>
            </div>
        </div>
    );
}

export default SeleccionModos;