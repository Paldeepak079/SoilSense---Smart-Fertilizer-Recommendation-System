/**
 * API Configuration
 * Centralized API URL configuration using environment variables
 */

// Get API URL from environment or use proxy in development
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

// Create configured axios instance (if you want to use axios globally)
import axios from 'axios';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// API endpoints
export const API_ENDPOINTS = {
    // Farmers
    farmers: '/api/farmers',
    farmerById: (id) => `/api/farmers/${id}`,

    // Soil Data
    soilData: '/api/soil-data',
    soilDataManual: '/api/soil-data/manual',
    soilDataUpload: (farmerId) => `/api/soil-data/upload/${farmerId}`,
    soilDataById: (id) => `/api/soil-data/${id}`,

    // Recommendations
    recommendations: '/api/recommendations/generate',

    // Soil Health Card
    soilHealthCardCSV: (recommendationId) => `/api/soil-health-card/${recommendationId}/csv`,
    soilHealthCardPDF: (recommendationId) => `/api/soil-health-card/${recommendationId}/pdf`,
    soilHealthCardExcel: (recommendationId) => `/api/soil-health-card/${recommendationId}/excel`,
};

export default API_BASE_URL;
