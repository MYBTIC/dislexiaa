import React, { useState } from 'react';
import Modal from './Modal';
import './EjemplosModal.css';

/**
 * Componente de demostración para mostrar los diferentes usos del Modal
 */
const EjemplosModal = () => {
    const [modalError, setModalError] = useState(false);
    const [modalExito, setModalExito] = useState(false);
    const [modalAdvertencia, setModalAdvertencia] = useState(false);
    const [modalInfo, setModalInfo] = useState(false);

    return (
        <div className="ejemplos-container">
            <h1>🎨 Ejemplos de Modales</h1>

            <div className="botones-grid">
                <button
                    className="btn-demo btn-error"
                    onClick={() => setModalError(true)}
                >
                    ❌ Mostrar Error
                </button>

                <button
                    className="btn-demo btn-exito"
                    onClick={() => setModalExito(true)}
                >
                    ✅ Mostrar Éxito
                </button>

                <button
                    className="btn-demo btn-advertencia"
                    onClick={() => setModalAdvertencia(true)}
                >
                    ⚠️ Mostrar Advertencia
                </button>

                <button
                    className="btn-demo btn-info"
                    onClick={() => setModalInfo(true)}
                >
                    ℹ️ Mostrar Información
                </button>
            </div>

            {/* MODAL DE ERROR */}
            <Modal
                mostrar={modalError}
                onCerrar={() => setModalError(false)}
                titulo="Error al cargar"
                mensaje="Error al cargar el juego. Intenta de nuevo."
                tipo="error"
                textoBoton="Entendido"
            />

            {/* MODAL DE ÉXITO */}
            <Modal
                mostrar={modalExito}
                onCerrar={() => setModalExito(false)}
                titulo="¡Excelente!"
                mensaje="¡Has completado todos los niveles correctamente!"
                tipo="exito"
                textoBoton="Continuar"
            />

            {/* MODAL DE ADVERTENCIA */}
            <Modal
                mostrar={modalAdvertencia}
                onCerrar={() => setModalAdvertencia(false)}
                titulo="Atención"
                mensaje="¿Estás seguro de que quieres salir? Perderás tu progreso."
                tipo="advertencia"
                textoBoton="Aceptar"
            />

            {/* MODAL DE INFORMACIÓN */}
            <Modal
                mostrar={modalInfo}
                onCerrar={() => setModalInfo(false)}
                titulo="Información"
                tipo="info"
            >
                {/* Contenido personalizado */}
                <div className="modal-contenido-personalizado">
                    <p tabIndex="0"><strong>Versión:</strong> 1.0.0</p>
                    <p tabIndex="0"><strong>Autor:</strong> Maximiliano Madrid</p>
                    <p tabIndex="0"><strong>Proyecto:</strong> Sistema de Dislexia</p>
                </div>
            </Modal>
        </div>
    );
};

export default EjemplosModal;
