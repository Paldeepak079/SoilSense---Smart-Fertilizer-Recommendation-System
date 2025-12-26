import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Container, Typography, Card, CardContent, Button, Box, AppBar, Toolbar,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    Paper, Chip, Alert, Grid, CircularProgress, Select, MenuItem, Tooltip
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import VerifiedIcon from '@mui/icons-material/Verified';
import DownloadIcon from '@mui/icons-material/Download';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';
import { LanguageContext } from '../App';
import { LANGUAGES, getText } from '../utils/translations';

function RecommendationView() {
    const navigate = useNavigate();
    const { farmerId, soilDataId } = useParams();
    const [farmer, setFarmer] = useState(null);
    const [soilData, setSoilData] = useState(null);
    const [recommendation, setRecommendation] = useState(null);
    const [additionalData, setAdditionalData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { language, setLanguage } = useContext(LanguageContext);

    useEffect(() => {
        fetchData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [farmerId, soilDataId]);

    const fetchData = async () => {
        try {
            const farmerRes = await axios.get(`/api/farmers/${farmerId}`);
            const soilRes = await axios.get(`/api/soil-data/${soilDataId}`);
            setFarmer(farmerRes.data);
            setSoilData(soilRes.data);

            const recRes = await axios.post('/api/recommendations/generate', {
                farmer_id: parseInt(farmerId),
                soil_data_id: parseInt(soilDataId),
            });
            setRecommendation(recRes.data);

            // Parse additional data from reasoning JSON
            try {
                const jsonMatch = recRes.data.reasoning.match(/\{[\s\S]*\}/);
                if (jsonMatch) {
                    const parsed = JSON.parse(jsonMatch[0]);
                    setAdditionalData(parsed);
                }
            } catch (e) {
                console.error('Failed to parse additional data:', e);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to load data');
        } finally {
            setLoading(false);
        }
    };

    // Advanced Health Score Logic (Distance from Optimal)
    const getStatus = (value, optimalMin, optimalMax, param = null) => {
        const optimalMid = (optimalMin + optimalMax) / 2;
        const tolerance = (optimalMax - optimalMin) / 2; // Half-width of optimal range

        let score = 0;
        let diff = Math.abs(value - optimalMid);

        // Special handling for pH (Optimal 6.5 - 7.5 usually)
        if (param === 'ph') {
            // pH logic: 6.5-7.5 is 100%. As it deviates, score drops.
            // tolerance ~ 0.5.
            if (value >= optimalMin && value <= optimalMax) score = 100;
            else {
                // Drop 20 points for every 0.5 deviation
                const deviation = diff - tolerance;
                score = Math.max(0, 100 - (deviation * 40));
            }
        } else {
            // General Logic
            if (value >= optimalMin && value <= optimalMax) {
                score = 100;
            } else {
                // Calculate percentage deviation
                // If value is double the max or half the min, score drops significantly
                // Simple linear drop off
                const maxDeviation = optimalMid; // e.g. if midpoint is 30, deviation of 30 (0 or 60) brings score low
                score = Math.max(0, 100 - ((diff / maxDeviation) * 100));
            }
        }

        let color = 'success';
        let label = 'Optimal';
        if (score < 40) { color = 'error'; label = 'Poor'; }
        else if (score < 75) { color = 'warning'; label = 'Average'; }

        // Override labels for low/high specific context
        if (value < optimalMin) label = 'Low';
        if (value > optimalMax) label = 'High';
        if (value >= optimalMin && value <= optimalMax) label = 'Optimal';

        return { label, color, percent: Math.round(score) };
    };

    // Helper for Circular Gauge
    const CircularGauge = ({ value, color, label }) => {
        // Map color string to hex
        const colorMap = {
            success: '#4CAF50',
            warning: '#FF9800',
            error: '#F44336',
            info: '#2196F3'
        };
        const hexColor = colorMap[color] || '#4CAF50';

        return (
            <Box sx={{ position: 'relative', display: 'inline-flex', flexDirection: 'column', alignItems: 'center' }}>
                <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                    <CircularProgress
                        variant="determinate"
                        value={100}
                        size={50}
                        sx={{ color: 'rgba(255, 255, 255, 0.1)' }}
                    />
                    <CircularProgress
                        variant="determinate"
                        value={value}
                        size={50}
                        sx={{
                            color: hexColor,
                            position: 'absolute',
                            left: 0,
                            '& .MuiCircularProgress-circle': { strokeLinecap: 'round' }
                        }}
                    />
                    <Box
                        sx={{
                            top: 0,
                            left: 0,
                            bottom: 0,
                            right: 0,
                            position: 'absolute',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                        }}
                    >
                        <Typography variant="caption" component="div" sx={{ color: hexColor, fontWeight: 'bold' }}>
                            {Math.round(value)}
                        </Typography>
                    </Box>
                </Box>
                <Typography variant="caption" sx={{ mt: 0.5, color: hexColor, fontWeight: 600 }}>
                    {label}
                </Typography>
            </Box>
        );
    };

    const handleDownloadCSV = () => {
        window.open(`http://localhost:8000/api/soil-health-card/${recommendation.id}/csv`, '_blank');
    };

    const handleDownloadPDF = () => {
        window.open(`http://localhost:8000/api/soil-health-card/${recommendation.id}/pdf`, '_blank');
    };

    const handleDownloadExcel = () => {
        window.open(`http://localhost:8000/api/soil-health-card/${recommendation.id}/excel`, '_blank');
    };

    if (loading) {
        return (
            <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <CircularProgress size={60} sx={{ color: '#4CAF50' }} />
                <Typography className="text-shimmer" sx={{ ml: 2 }}>Loading Analysis...</Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ minHeight: '100vh', pb: 8 }}>
            <AppBar position="sticky" elevation={0} sx={{ top: 0, zIndex: 1100, backgroundColor: 'rgba(0,0,0,0.2)', backdropFilter: 'blur(20px)', borderBottom: 'none' }}>
                <Toolbar>
                    <img src="/logo.png" alt="SoilSense Logo"
                        style={{ height: '60px', marginRight: '16px' }} />
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        <span className="text-shimmer" style={{ fontSize: '1.5rem' }}>{getText('soil_health_card', language)}</span>
                    </Typography>
                    <Select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        size="small"
                        sx={{
                            color: '#4CAF50',
                            mr: 2,
                            '.MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(76, 175, 80, 0.5)' },
                            '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: '#4CAF50' }
                        }}
                    >
                        {LANGUAGES.map((lang) => (
                            <MenuItem key={lang.code} value={lang.code}>{lang.nativeName}</MenuItem>
                        ))}
                    </Select>
                    <Button color="inherit" variant="outlined" startIcon={<DownloadIcon className="neon-icon" />}
                        onClick={handleDownloadCSV} sx={{ mr: 1, borderColor: 'rgba(76, 175, 80, 0.5)', borderRadius: '20px' }}>
                        CSV
                    </Button>
                    <Button color="inherit" variant="outlined" startIcon={<DownloadIcon className="neon-icon" />}
                        onClick={handleDownloadPDF} sx={{ mr: 1, borderColor: 'rgba(255, 152, 0, 0.5)', borderRadius: '20px' }}>
                        PDF
                    </Button>
                    <Button color="inherit" variant="outlined" startIcon={<DownloadIcon className="neon-icon" />}
                        onClick={handleDownloadExcel} sx={{ mr: 2, borderColor: 'rgba(33, 150, 243, 0.5)', borderRadius: '20px' }}>
                        Excel
                    </Button>
                    <Button color="inherit" startIcon={<ArrowBackIcon />} onClick={() => navigate('/')} sx={{ borderRadius: '20px' }}>
                        {getText('back_dashboard', language)}
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4 }} component={motion.div} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
                {error && <Alert severity="error" sx={{ mb: 2, backgroundColor: 'rgba(211, 47, 47, 0.1)', backdropFilter: 'blur(10px)' }}>{typeof error === 'string' ? error : 'Failed to load data.'}</Alert>}

                {/* Farmer Info */}
                {farmer && (
                    <Card className="premium-card" sx={{ mb: 4 }}>
                        <CardContent>
                            <Typography variant="h4" className="text-shimmer" sx={{ mb: 1 }}>{farmer.name}</Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={12} md={6}>
                                    <Typography variant="body1" sx={{ color: '#e0e0e0', fontSize: '1.1rem' }}>
                                        📍 {farmer.village}, {farmer.district}, {farmer.state}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} md={6}>
                                    <Typography variant="body1" sx={{ color: '#e0e0e0', fontSize: '1.1rem' }}>
                                        🌾 <strong>{farmer.field_area} ha</strong> | {farmer.crop_name} ({farmer.crop_season})
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                )}

                {/* TABLE 1: Soil Health Summary with GAUGES */}
                {soilData && (
                    <Card className="premium-card" sx={{ mb: 4 }}>
                        <CardContent>
                            <Typography variant="h5" sx={{ mb: 3, color: '#4CAF50', fontWeight: 'bold' }}>
                                🔬 {getText('soil_health_analysis', language)}
                            </Typography>
                            <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', boxShadow: 'none' }}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold', fontSize: '1.1rem' }}>{getText('parameter', language)}</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold', fontSize: '1.1rem' }}>{getText('value', language)}</TableCell>
                                            <TableCell align="center" sx={{ color: '#81C784', fontWeight: 'bold', fontSize: '1.1rem' }}>{getText('health_score', language)}</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {(() => {
                                            // Crop-specific optimal ranges
                                            const CROP_RANGES = {
                                                'Wheat': { n: [200, 300], p: [20, 40], k: [150, 250], ph: [6.0, 7.5] },
                                                'Rice': { n: [250, 350], p: [25, 45], k: [180, 280], ph: [5.5, 7.0] },
                                                'Cotton': { n: [220, 320], p: [30, 50], k: [200, 300], ph: [6.0, 8.0] },
                                                'Sugarcane': { n: [300, 400], p: [40, 60], k: [250, 350], ph: [6.5, 7.5] },
                                                'Maize': { n: [200, 300], p: [20, 50], k: [150, 250], ph: [5.8, 7.5] },
                                                // Default
                                                'default': { n: [200, 400], p: [20, 60], k: [150, 300], ph: [6.0, 7.5] }
                                            };

                                            // Normalized lookup
                                            const cropName = farmer.crop_name ? farmer.crop_name.split(' ')[0] : 'default'; // Simple match
                                            const range = CROP_RANGES[cropName] || CROP_RANGES['default'];

                                            return [
                                                { label: 'Nitrogen (N)', value: soilData.nitrogen, unit: 'mg/kg', param: 'nitrogen', low: range.n[0], high: range.n[1] },
                                                { label: 'Phosphorus (P)', value: soilData.phosphorus, unit: 'mg/kg', param: 'phosphorus', low: range.p[0], high: range.p[1] },
                                                { label: 'Potassium (K)', value: soilData.potassium, unit: 'mg/kg', param: 'potassium', low: range.k[0], high: range.k[1] },
                                                { label: 'pH Level', value: soilData.ph, unit: '', param: 'ph', low: range.ph[0], high: range.ph[1] },
                                                { label: 'EC (Salinity)', value: soilData.ec, unit: 'dS/m', param: 'ec', low: 0, high: 2.0 }, // General ag limit
                                                { label: 'Organic Carbon', value: soilData.organic_carbon, unit: '%', param: 'oc', low: 0.5, high: 0.75 },
                                            ].map((row, idx) => {
                                                if (row.value === null || row.value === undefined) return null;
                                                const status = getStatus(row.value, row.low, row.high, row.param);
                                                return (
                                                    <TableRow key={idx} className="border-glow" sx={{ '&:hover': { backgroundColor: 'rgba(76, 175, 80, 0.1)' } }}>
                                                        <TableCell sx={{ color: '#fff', fontSize: '1.1rem', py: 2 }}>{row.label}</TableCell>
                                                        <TableCell align="right" sx={{ color: '#fff', fontSize: '1.2rem', fontWeight: 600 }}>
                                                            {row.value} {row.unit && <span style={{ fontSize: '0.9rem', color: '#aaa' }}>{row.unit}</span>}
                                                        </TableCell>
                                                        <TableCell align="center">
                                                            <CircularGauge value={status.percent} color={status.color} label={status.label} />
                                                        </TableCell>
                                                    </TableRow>
                                                );
                                            });
                                        })()}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                )}

                {/* TABLE 2: Fertilizer Recommendations */}
                {recommendation && additionalData && (
                    <Card className="premium-card" sx={{ mb: 4 }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                                <Typography variant="h5" sx={{ flexGrow: 1, color: '#4CAF50', fontWeight: 'bold' }}>
                                    💊 {getText('fertilizer_plan', language)}
                                </Typography>
                                <Chip icon={<VerifiedIcon className="neon-icon" />} label={getText('govt_verified', language)}
                                    sx={{ backgroundColor: 'rgba(76, 175, 80, 0.2)', color: '#4CAF50', fontWeight: 'bold' }} />
                            </Box>

                            <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', boxShadow: 'none' }}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('fertilizer', language)}</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('quantity', language)}</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold' }}>Bags (50kg)</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold' }}>Cost</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {additionalData.fertilizer_details?.map((fert, index) => {
                                            const totalQuantity = fert.quantity_total || (fert.quantity_kg_per_hectare * farmer.field_area);
                                            const bagsRequired = Math.ceil(totalQuantity / 50);

                                            return (
                                                <TableRow key={index} className="border-glow" sx={{ '&:hover': { backgroundColor: 'rgba(76, 175, 80, 0.1)' } }}>
                                                    <TableCell sx={{ color: '#fff', fontSize: '1.1rem', fontWeight: 500 }}>
                                                        {fert.fertilizer}
                                                        {!fert.is_verified && (
                                                            <Tooltip title="Price not verified by Govt">
                                                                <WarningIcon sx={{ color: '#FF9800', fontSize: '1rem', ml: 1, verticalAlign: 'middle' }} />
                                                            </Tooltip>
                                                        )}
                                                    </TableCell>
                                                    <TableCell align="right" sx={{ color: '#e0e0e0', fontSize: '1.1rem' }}>
                                                        {totalQuantity.toFixed(2)} <span style={{ fontSize: '0.8rem', color: '#888' }}>kg</span>
                                                    </TableCell>
                                                    <TableCell align="right" sx={{ color: '#4CAF50', fontSize: '1.1rem', fontWeight: 'bold' }}>
                                                        {bagsRequired}
                                                    </TableCell>
                                                    <TableCell align="right" sx={{ color: '#81C784', fontSize: '1.1rem' }}>
                                                        {fert.is_verified ? `₹${fert.cost}` : (
                                                            <span style={{ color: '#FF9800', fontSize: '0.9rem' }}>
                                                                {getText('price_na', language)}
                                                            </span>
                                                        )}
                                                    </TableCell>
                                                </TableRow>
                                            );
                                        })}

                                        <TableRow sx={{ backgroundColor: 'rgba(76, 175, 80, 0.2)' }}>
                                            <TableCell sx={{ color: '#4CAF50', fontWeight: 'bold', fontSize: '1.2rem' }}>{getText('total_estimate', language)}</TableCell>
                                            <TableCell colSpan={2} />
                                            <TableCell align="right" sx={{ color: '#4CAF50', fontWeight: 'bold', fontSize: '1.5rem', textShadow: '0 0 10px rgba(76, 175, 80, 0.5)' }}>
                                                ₹{recommendation.estimated_cost?.toLocaleString()}
                                            </TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                )}

                {/* TABLE 3: Application Schedule */}
                {additionalData?.application_schedule && (
                    <Card className="premium-card" sx={{ mb: 4 }} component={motion.div} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
                        <CardContent>
                            <Typography variant="h5" sx={{ mb: 3, color: '#4CAF50', fontWeight: 'bold' }}>
                                📅 {getText('app_schedule', language)}
                            </Typography>
                            <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', boxShadow: 'none' }}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('stage', language)}</TableCell>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('time', language)}</TableCell>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('fertilizer', language)}</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold' }}>Quantity (%)</TableCell>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('note', language)}</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {additionalData.application_schedule.map((stage, index) => (
                                            <TableRow key={index} className="border-glow" sx={{ '&:hover': { backgroundColor: 'rgba(76, 175, 80, 0.1)' } }}>
                                                <TableCell sx={{ color: '#fff', fontWeight: 500 }}>{stage.stage}</TableCell>
                                                <TableCell sx={{ color: '#e0e0e0' }}>{stage.time}</TableCell>
                                                <TableCell sx={{ color: '#81C784' }}>{stage.fertilizer}</TableCell>
                                                <TableCell align="right" sx={{ color: '#e0e0e0' }}>{stage.quantity_percent}%</TableCell>
                                                <TableCell sx={{ color: '#e0e0e0', fontSize: '0.9rem' }}>{stage.note}</TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                )}

                {/* TABLE 4: Soil Improvement Advisory */}
                {additionalData?.soil_improvements && (
                    <Card className="premium-card" sx={{ mb: 4 }} component={motion.div} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }}>
                        <CardContent>
                            <Typography variant="h5" sx={{ mb: 3, color: '#4CAF50', fontWeight: 'bold' }}>
                                🌱 {getText('improvement_advisory', language)}
                            </Typography>
                            <TableContainer component={Paper} sx={{ backgroundColor: 'transparent', boxShadow: 'none' }}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('issue', language)}</TableCell>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('recommendation', language)}</TableCell>
                                            <TableCell align="right" sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('quantity', language)}</TableCell>
                                            <TableCell sx={{ color: '#81C784', fontWeight: 'bold' }}>{getText('purpose', language)}</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {additionalData.soil_improvements.map((imp, index) => (
                                            <TableRow key={index} className="border-glow" sx={{ '&:hover': { backgroundColor: 'rgba(76, 175, 80, 0.1)' } }}>
                                                <TableCell sx={{ color: '#fff', fontWeight: 500 }}>{imp.issue}</TableCell>
                                                <TableCell sx={{ color: '#81C784' }}>{imp.recommendation}</TableCell>
                                                <TableCell align="right" sx={{ color: '#e0e0e0' }}>{imp.quantity}</TableCell>
                                                <TableCell sx={{ color: '#e0e0e0', fontSize: '0.9rem' }}>{imp.purpose}</TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                )}

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

export default RecommendationView;
