import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Container, Typography, Card, CardContent, Button, Grid, Box,
    List, ListItem, ListItemText, AppBar, Toolbar, Select, MenuItem, Chip, IconButton,
} from '@mui/material';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ScienceIcon from '@mui/icons-material/Science';
import MemoryIcon from '@mui/icons-material/Memory';
import DescriptionIcon from '@mui/icons-material/Description';
import StoreIcon from '@mui/icons-material/Store';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import MoneyOffIcon from '@mui/icons-material/MoneyOff';
import ConstructionIcon from '@mui/icons-material/Construction';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';
import { LanguageContext } from '../App';
import { LANGUAGES, getText } from '../utils/translations';

function Dashboard() {
    const navigate = useNavigate();
    const [farmers, setFarmers] = useState([]);
    const [loading, setLoading] = useState(true);
    const { language, setLanguage } = useContext(LanguageContext);

    useEffect(() => {
        fetchFarmers();
    }, []);

    const fetchFarmers = async () => {
        try {
            const response = await axios.get('/api/farmers');
            setFarmers(response.data);
        } catch (error) {
            console.error('Error fetching farmers:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleEditFarmer = (farmerId, e) => {
        e.stopPropagation();
        navigate(`/register-farmer?edit=${farmerId}`);
    };

    const handleDeleteFarmer = async (farmerId, e) => {
        e.stopPropagation();
        if (window.confirm('Are you sure you want to delete this farmer?')) {
            try {
                await axios.delete(`/api/farmers/${farmerId}`);
                fetchFarmers(); // Refresh list
            } catch (error) {
                console.error('Error deleting farmer:', error);
                alert('Failed to delete farmer');
            }
        }
    };

    const features = [
        { icon: <MemoryIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'iot_integration', color: '#2196F3', available: true },
        { icon: <ScienceIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'ml_recommendations', color: '#4CAF50', available: true },
        { icon: <DescriptionIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'soil_health_cards', color: '#FF9800', available: true },
        { icon: <StoreIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'dealer_locator', color: '#9C27B0', available: false },
        { icon: <MoneyOffIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'subsidy_calc', color: '#F44336', available: false },
        { icon: <AccountBalanceIcon sx={{ fontSize: 40 }} className="neon-icon" />, key: 'govt_integration', color: '#00BCD4', available: false },
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { y: 0, opacity: 1 }
    };

    return (
        <Box sx={{ minHeight: '100vh', backgroundColor: '#000000' }}>
            <AppBar position="sticky" elevation={0} sx={{ top: 0, zIndex: 1100, backgroundColor: 'rgba(0, 0, 0, 0.2)', backdropFilter: 'blur(20px)', borderBottom: 'none' }}>
                <Toolbar>
                    <img src="/logo.png" alt="SoilSense" style={{ height: '80px', marginRight: '16px' }} />
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: '#4CAF50', fontWeight: 600, textShadow: '0 0 10px rgba(76, 175, 80, 0.5)' }}>
                        SoilSense - Smart Fertilizer Recommendation System
                    </Typography>
                    <Select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        sx={{
                            color: '#4CAF50',
                            '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(76, 175, 80, 0.5)' },
                            '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#4CAF50' }
                        }}
                    >
                        {LANGUAGES.map((lang) => (
                            <MenuItem key={lang.code} value={lang.code}>{lang.nativeName}</MenuItem>
                        ))}
                    </Select>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4, pb: 4 }} component={motion.div} variants={containerVariants} initial="hidden" animate="visible">
                <Typography variant="h4" gutterBottom className="text-shimmer" sx={{ fontWeight: 'bold', mb: 4 }} component={motion.h4} variants={itemVariants}>
                    {getText('dashboard', language)}
                </Typography>

                <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                        <Card className="premium-card" sx={{ height: '100%' }} component={motion.div} variants={itemVariants}>
                            <CardContent>
                                <Typography variant="h5" gutterBottom sx={{ color: '#4CAF50' }}>
                                    {getText('quick_actions', language)}
                                </Typography>
                                <Box sx={{ mt: 2 }}>
                                    <Button
                                        variant="contained"
                                        fullWidth
                                        startIcon={<PersonAddIcon />}
                                        onClick={() => navigate('/register-farmer')}
                                        sx={{ mb: 2, backgroundColor: '#4CAF50', '&:hover': { backgroundColor: '#45a049' } }}
                                    >
                                        {getText('register_farmer', language)}
                                    </Button>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <Card className="premium-card" sx={{ height: '100%' }} component={motion.div} variants={itemVariants}>
                            <CardContent>
                                <Typography variant="h5" gutterBottom sx={{ color: '#4CAF50' }}>
                                    {getText('recent_farmers', language)}
                                </Typography>
                                {loading ? (
                                    <Typography>Loading...</Typography>
                                ) : farmers.length === 0 ? (
                                    <Typography sx={{ color: '#e0e0e0', mt: 2 }}>
                                        No farmers registered yet.
                                    </Typography>
                                ) : (
                                    <List>
                                        {farmers.slice(0, 5).map((farmer) => (
                                            <ListItem
                                                key={farmer.id}
                                                button
                                                onClick={() => navigate(`/soil-data-entry/${farmer.id}`)}
                                                sx={{
                                                    backgroundColor: '#000000',
                                                    mb: 1,
                                                    borderRadius: 1,
                                                    border: '1px solid rgba(76, 175, 80, 0.2)',
                                                    '&:hover': { backgroundColor: 'rgba(76, 175, 80, 0.1)' },
                                                    pr: 10,
                                                    cursor: 'pointer'
                                                }}
                                                secondaryAction={
                                                    <Box>
                                                        <IconButton
                                                            edge="end"
                                                            onClick={(e) => handleEditFarmer(farmer.id, e)}
                                                            sx={{ color: '#4CAF50', mr: 1 }}
                                                        >
                                                            <EditIcon />
                                                        </IconButton>
                                                        <IconButton
                                                            edge="end"
                                                            onClick={(e) => handleDeleteFarmer(farmer.id, e)}
                                                            sx={{ color: '#f44336' }}
                                                        >
                                                            <DeleteIcon />
                                                        </IconButton>
                                                    </Box>
                                                }
                                            >
                                                <ListItemText
                                                    primary={farmer.name}
                                                    secondary={`${farmer.village}, ${farmer.district}`}
                                                    primaryTypographyProps={{ style: { color: '#4CAF50', fontWeight: 'bold' } }}
                                                    secondaryTypographyProps={{ style: { color: '#e0e0e0' } }}
                                                />
                                            </ListItem>
                                        ))}
                                    </List>
                                )}
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12}>
                        <Typography variant="h5" gutterBottom sx={{ color: '#4CAF50', mt: 2, mb: 2 }} component={motion.h5} variants={itemVariants}>
                            {getText('system_features', language)}
                        </Typography>
                    </Grid>

                    {features.map((feature, idx) => (
                        <Grid item xs={12} sm={6} md={4} key={idx} component={motion.div} variants={itemVariants} whileHover={{ scale: 1.05 }} transition={{ type: 'spring', stiffness: 300 }}>
                            <Card className="premium-card" sx={{ height: '100%', position: 'relative', opacity: feature.available ? 1 : 0.6 }}>
                                <CardContent sx={{ textAlign: 'center' }}>
                                    <Box sx={{ color: feature.color, mb: 2 }}>{feature.icon}</Box>
                                    <Typography variant="h6" sx={{ color: '#fff', mb: 1, fontWeight: 'bold' }}>
                                        {getText(feature.key, language)}
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: '#e0e0e0' }}>
                                        {getText(`${feature.key}_desc`, language)}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>

            {/* Footer */}
            <Box
                sx={{
                    textAlign: 'center',
                    py: 3,
                    borderTop: '1px solid rgba(76, 175, 80, 0.2)',
                    backgroundColor: 'rgba(0, 0, 0, 0.3)',
                    backdropFilter: 'blur(10px)'
                }}
            >
                <Typography
                    variant="body2"
                    sx={{
                        color: '#81C784',
                        fontWeight: 500,
                        letterSpacing: '0.5px'
                    }}
                >
                    Crafted by Team_MADTech
                </Typography>
            </Box>
        </Box>
    );
}

export default Dashboard;
