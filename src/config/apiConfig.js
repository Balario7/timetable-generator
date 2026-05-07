// API Configuration - Centralized Backend Connection
// This file manages all backend API endpoints

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// Backend API Endpoints
export const API_ENDPOINTS = {
  // Courses
  GET_COURSES: `${API_BASE_URL}/get-courses`,
  ADD_COURSE: `${API_BASE_URL}/add-course`,

  // Constraints
  GET_CONSTRAINTS: `${API_BASE_URL}/get-constraints`,
  ADD_CONSTRAINTS: `${API_BASE_URL}/add-constraints`,

  // Timetable Generation
  GENERATE_TIMETABLE: `${API_BASE_URL}/generate-timetable`,
};

// Helper function to get full API URL
export const getAPIUrl = (endpoint) => {
  return API_ENDPOINTS[endpoint] || API_BASE_URL;
};

export default API_ENDPOINTS;
