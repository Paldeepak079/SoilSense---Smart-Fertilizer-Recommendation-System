import React, { useState, createContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Dashboard from './pages/Dashboard';
import FarmerRegistration from './pages/FarmerRegistration';
import SoilDataEntry from './pages/SoilDataEntry';
import RecommendationView from './pages/RecommendationView';
import ComingSoon from './pages/ComingSoon';

// Language Context
export const LanguageContext = createContext();

// Pure Black Premium Theme Configuration
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4CAF50',
    },
    secondary: {
      main: '#81C784',
    },
    background: {
      default: 'transparent',
      paper: 'rgba(20, 20, 20, 0.6)',
    },
    text: {
      primary: '#ffffff',
      secondary: '#e0e0e0',
    },
  },
  typography: {
    fontFamily: '"Outfit", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(20, 20, 20, 0.6)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(76, 175, 80, 0.2)',
          borderRadius: '16px',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(20, 20, 20, 0.6)',
          backgroundImage: 'none',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderBottom: '1px solid rgba(76, 175, 80, 0.3)',
          backdropFilter: 'blur(20px)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '10px',
        },
      },
    },
  },
});

function App() {
  const [language, setLanguage] = useState('en');

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/register-farmer" element={<FarmerRegistration />} />
            <Route path="/soil-data-entry/:farmerId" element={<SoilDataEntry />} />
            <Route path="/recommendation/:farmerId/:soilDataId" element={<RecommendationView />} />
            <Route path="/coming-soon" element={<ComingSoon />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </LanguageContext.Provider>
  );
}

export default App;
