// Configuración de la API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

export const API_ENDPOINTS = {
    ANAGRAMA: `${API_BASE_URL}/juego1/`,
    SILABAS: `${API_BASE_URL}/juego2/`,
    ORACION: `${API_BASE_URL}/oracion/`,
};

export default API_BASE_URL;
