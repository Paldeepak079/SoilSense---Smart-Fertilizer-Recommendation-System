import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, Button, Grid, Chip } from '@mui/material';
import ConstructionIcon from '@mui/icons-material/Construction';
import StoreIcon from '@mui/icons-material/Store';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import MoneyOffIcon from '@mui/icons-material/MoneyOff';

function ComingSoon() {
    const [selectedFeature, setSelectedFeature] = useState(null);

    const features = [
        {
            id: 'dealer',
            title: 'Dealer Locator',
            titleHi: 'डीलर खोजक',
            icon: <StoreIcon sx={{ fontSize: 60 }} />,
            message: "🌾 Finding the nearest dealer who sells dreams in bags!",
            messageHi: "🌾 हम आपके लिए सबसे नजदीकी डीलर ढूंढ रहे हैं!",
            funFact: "Fun Fact: Our GPS is so good, it can even find fertilizer shops that don't exist yet! 😄",
            eta: "ETA: 2 weeks",
            color: '#FF9800'
        },
        {
            id: 'subsidy',
            title: 'Subsidy Calculator',
            titleHi: 'सब्सिडी कैलकुलेटर',
            icon: <MoneyOffIcon sx={{ fontSize: 60 }} />,
            message: "💰 Our calculator is busy counting all the money you'll save!",
            messageHi: "💰 हमारा कैलकुलेटर आपकी बचत गिनने में व्यस्त है!",
            funFact: "Insider Info: It's SO excited about your savings, it needs a cooldown period! 🧊",
            eta: "ETA: 1 week",
            color: '#4CAF50'
        },
        {
            id: 'govt',
            title: 'Government Integration',
            titleHi: 'सरकारी एकीकरण',
            icon: <AccountBalanceIcon sx={{ fontSize: 60 }} />,
            message: "🏛️ Teaching government servers to speak farmer language!",
            messageHi: "🏛️ सरकारी सर्वर को किसान भाषा सिखा रहे हैं!",
            funFact: "Behind the scenes: Currently convincing bureaucracy to move faster than a tractor! 🚜",
            eta: "ETA: 3 weeks",
            color: '#2196F3'
        }
    ];

    return (
        <Box sx={{ minHeight: '100vh', backgroundColor: '#000000', p: 4 }}>
            <Typography variant="h3" className="text-shimmer" sx={{ textAlign: 'center', mb: 4, color: '#4CAF50' }}>
                🚧 Exciting Features Coming Soon! 🚧
            </Typography>

            <Typography variant="h6" sx={{ textAlign: 'center', mb: 6, color: '#e0e0e0' }}>
                जल्द आ रहे हैं रोमांचक फीचर्स!
            </Typography>

            <Grid container spacing={4}>
                {features.map((feature) => (
                    <Grid item xs={12} md={4} key={feature.id}>
                        <Card
                            className="premium-card"
                            sx={{
                                height: '100%',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease',
                                border: selectedFeature === feature.id ? `2px solid ${feature.color}` : 'none',
                                '&:hover': {
                                    transform: 'translateY(-10px)',
                                    boxShadow: `0 10px 30px ${feature.color}40`
                                }
                            }}
                            onClick={() => setSelectedFeature(feature.id === selectedFeature ? null : feature.id)}
                        >
                            <CardContent sx={{ textAlign: 'center' }}>
                                <Box sx={{ color: feature.color, mb: 2 }}>{feature.icon}</Box>

                                <Typography variant="h5" sx={{ color: '#fff', mb: 1, fontWeight: 'bold' }}>
                                    {feature.title}
                                </Typography>

                                <Typography variant="body2" sx={{ color: '#81C784', mb: 2, fontSize: '0.9rem' }}>
                                    {feature.titleHi}
                                </Typography>

                                <Chip
                                    label={feature.eta}
                                    sx={{
                                        backgroundColor: feature.color,
                                        color: '#000',
                                        fontWeight: 'bold',
                                        mb: 3
                                    }}
                                />

                                <Typography variant="body1" sx={{ color: '#e0e0e0', mb: 2, minHeight: '60px' }}>
                                    {feature.message}
                                </Typography>

                                <Typography variant="caption" sx={{ color: '#81C784', fontStyle: 'italic', display: 'block', mb: 2 }}>
                                    {feature.messageHi}
                                </Typography>

                                {selectedFeature === feature.id && (
                                    <Box sx={{
                                        mt: 3,
                                        p: 2,
                                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                                        borderRadius: 2,
                                        animation: 'fadeIn 0.5s'
                                    }}>
                                        <Typography variant="body2" sx={{ color: '#4CAF50', fontWeight: 'bold' }}>
                                            {feature.funFact}
                                        </Typography>
                                    </Box>
                                )}

                                <Button
                                    variant="outlined"
                                    startIcon={<ConstructionIcon />}
                                    sx={{
                                        mt: 3,
                                        color: feature.color,
                                        borderColor: feature.color,
                                        '&:hover': {
                                            borderColor: feature.color,
                                            backgroundColor: `${feature.color}20`
                                        }
                                    }}
                                    fullWidth
                                >
                                    Under Construction
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Box sx={{ mt: 6, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ color: '#4CAF50', mb: 2 }}>
                    🎉 Want to be notified when these launch?
                </Typography>
                <Typography variant="body2" sx={{ color: '#e0e0e0' }}>
                    Stay tuned! We're working day and night (mostly day, we need sleep too! 😴)
                </Typography>
            </Box>

            <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `}</style>
        </Box>
    );
}

export default ComingSoon;
