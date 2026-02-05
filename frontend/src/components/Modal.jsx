import React, { useEffect, useRef } from 'react';
import './Modal.css';

/**
 * Componente Modal reutilizable con accesibilidad completa
 * @param {boolean} mostrar - Controla si el modal está visible
 * @param {function} onCerrar - Función para cerrar el modal
 * @param {string} titulo - Título del modal
 * @param {string} mensaje - Mensaje principal
 * @param {string} tipo - Tipo de modal: 'error', 'exito', 'advertencia', 'info'
 * @param {string} textoBoton - Texto del botón (opcional, por defecto "OK")
 */
const Modal = ({
    mostrar,
    onCerrar,
    titulo = "Mensaje",
    mensaje,
    tipo = "info",
    textoBoton = "OK",
    children
}) => {
    const botonRef = useRef(null);
    const modalRef = useRef(null);

    // Íconos según el tipo
    const iconos = {
        error: "❌",
        exito: "✅",
        advertencia: "⚠️",
        info: "ℹ️"
    };

    // Focus trap y manejo de tecla Escape
    useEffect(() => {
        if (!mostrar) return;

        // Guardar el elemento activo anterior para restaurar el focus después
        const elementoAnterior = document.activeElement;

        // Enfocar el botón cuando se abre el modal
        const focusTimeout = setTimeout(() => {
            botonRef.current?.focus();
        }, 100);

        // Manejar tecla Escape para cerrar
        const manejarEscape = (e) => {
            if (e.key === 'Escape') {
                onCerrar();
            }
        };

        // Manejar focus trap
        const manejarTab = (e) => {
            if (e.key !== 'Tab' || !modalRef.current) return;

            const elementosFocusables = modalRef.current.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );

            const primerElemento = elementosFocusables[0];
            const ultimoElemento = elementosFocusables[elementosFocusables.length - 1];

            if (e.shiftKey) {
                // Si presiona Shift+Tab en el primer elemento, ir al último
                if (document.activeElement === primerElemento) {
                    e.preventDefault();
                    ultimoElemento?.focus();
                }
            } else {
                // Si presiona Tab en el último elemento, ir al primero
                if (document.activeElement === ultimoElemento) {
                    e.preventDefault();
                    primerElemento?.focus();
                }
            }
        };

        document.addEventListener('keydown', manejarEscape);
        document.addEventListener('keydown', manejarTab);

        return () => {
            clearTimeout(focusTimeout);
            document.removeEventListener('keydown', manejarEscape);
            document.removeEventListener('keydown', manejarTab);
            // Restaurar el focus al elemento anterior
            elementoAnterior?.focus();
        };
    }, [mostrar, onCerrar]);

    if (!mostrar) return null;

    return (
        <div
            className="modal-overlay"
            onClick={onCerrar}
            role="presentation"
        >
            <div
                ref={modalRef}
                className={`modal-contenido modal-${tipo}`}
                onClick={(e) => e.stopPropagation()}
                role="dialog"
                aria-modal="true"
                aria-labelledby="modal-titulo"
                aria-describedby={mensaje ? "modal-mensaje" : undefined}
                tabIndex="-1"
            >
                <div className="modal-header">
                    <span className="modal-icono" aria-hidden="true" tabIndex="0">{iconos[tipo]}</span>
                    <h2 id="modal-titulo" className="modal-titulo" tabIndex="0">{titulo}</h2>
                </div>

                <div className="modal-body">
                    {mensaje && <p id="modal-mensaje" className="modal-mensaje" tabIndex="0">{mensaje}</p>}
                    {children}
                </div>

                <div className="modal-footer">
                    <button
                        ref={botonRef}
                        className="modal-boton"
                        onClick={onCerrar}
                        aria-label={`${textoBoton}, cerrar diálogo`}
                    >
                        {textoBoton}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Modal;
