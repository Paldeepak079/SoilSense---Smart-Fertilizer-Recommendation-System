import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
    Container,
    Typography,
    Card,
    CardContent,
    TextField,
    Button,
    Grid,
    Box,
    AppBar,
    Toolbar,
    MenuItem,
    Alert,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import EditIcon from '@mui/icons-material/Edit';
import axios from 'axios';


function FarmerRegistration() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const editId = searchParams.get('edit');
    const isEditMode = Boolean(editId);

    const [formData, setFormData] = useState({
        name: '',
        mobile: '',
        village: '',
        district: '',
        state: '',
        field_area: '',
        crop_name: '',
        crop_season: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(isEditMode);

    const seasons = ['Kharif', 'Rabi', 'Zaid'];

    useEffect(() => {
        if (isEditMode) {
            fetchFarmerData();
        }
    }, [editId]);

    const fetchFarmerData = async () => {
        try {
            const response = await axios.get(`/api/farmers/${editId}`);
            setFormData(response.data);
            setLoading(false);
        } catch (error) {
            setError('Failed to load farmer data');
            setLoading(false);
            console.error(error);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            let response;
            if (isEditMode) {
                // Update existing farmer
                response = await axios.put(`/api/farmers/${editId}`, {
                    ...formData,
                    field_area: parseFloat(formData.field_area),
                });
            } else {
                // Create new farmer
                response = await axios.post('/api/farmers', {
                    ...formData,
                    field_area: parseFloat(formData.field_area),
                });
            }

            setSuccess(true);
            setTimeout(() => {
                if (isEditMode) {
                    navigate('/'); // Go back to dashboard after edit
                } else {
                    navigate(`/soil-data-entry/${response.data.id}`);
                }
            }, 1500);
        } catch (err) {
            setError(err.response?.data?.detail || `Failed to ${isEditMode ? 'update' : 'register'} farmer. Please try again.`);
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#000000' }}>
                <Typography variant="h5" sx={{ color: '#4CAF50' }}>Loading...</Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ minHeight: '100vh', backgroundColor: '#000000' }}>
            <AppBar position="static">
                <Toolbar>
                    <img
                        src="/logo.png"
                        alt="SoilSense Logo"
                        style={{
                            height: '48px',
                            marginRight: '16px',
                            filter: 'drop-shadow(0 0 10px rgba(76, 175, 80, 0.5))'
                        }}
                    />
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{
                            flexGrow: 1,
                            fontWeight: 600,
                            textShadow: '0 0 10px rgba(76, 175, 80, 0.5)'
                        }}
                    >
                        <span className="text-shimmer">{isEditMode ? 'Edit Farmer Details' : 'Farmer Registration'}</span>
                    </Typography>
                    <Button
                        color="inherit"
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/')}
                        sx={{ borderColor: 'rgba(76, 175, 80, 0.5)' }}
                    >
                        Back to Dashboard
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="md" sx={{ mt: 4, pb: 4 }}>
                <Card className="premium-card">
                    <CardContent sx={{ p: 4 }}>
                        <Typography
                            variant="h4"
                            gutterBottom
                            className="text-shimmer"
                            sx={{ mb: 3, textAlign: 'center' }}
                        >
                            {isEditMode ? 'Edit Farmer Information' : 'Register New Farmer'}
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 2, backgroundColor: 'rgba(211, 47, 47, 0.1)' }}>
                                {error}
                            </Alert>
                        )}

                        {success && (
                            <Alert severity="success" sx={{ mb: 2, backgroundColor: 'rgba(76, 175, 80, 0.1)' }}>
                                Farmer {isEditMode ? 'updated' : 'registered'} successfully! Redirecting...
                            </Alert>
                        )}

                        <form onSubmit={handleSubmit}>
                            <Grid container spacing={3}>
                                <Grid item xs={12} md={6}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="Farmer Name"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                    />
                                </Grid>

                                <Grid item xs={12} md={6}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="Mobile Number"
                                        name="mobile"
                                        value={formData.mobile}
                                        onChange={handleChange}
                                        inputProps={{ pattern: '[0-9]{10}', maxLength: 10 }}
                                    />
                                </Grid>

                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="Village"
                                        name="village"
                                        value={formData.village}
                                        onChange={handleChange}
                                    />
                                </Grid>

                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="District"
                                        name="district"
                                        value={formData.district}
                                        onChange={handleChange}
                                    />
                                </Grid>

                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="State"
                                        name="state"
                                        value={formData.state}
                                        onChange={handleChange}
                                    />
                                </Grid>

                                <Grid item xs={12} md={6}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="Field Area (hectares)"
                                        name="field_area"
                                        type="number"
                                        value={formData.field_area}
                                        onChange={handleChange}
                                        inputProps={{ min: 0, step: 0.1 }}
                                    />
                                </Grid>

                                <Grid item xs={12} md={6}>
                                    <TextField
                                        fullWidth
                                        required
                                        label="Crop Name"
                                        name="crop_name"
                                        value={formData.crop_name}
                                        onChange={handleChange}
                                    />
                                </Grid>

                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        required
                                        select
                                        label="Crop Season"
                                        name="crop_season"
                                        value={formData.crop_season}
                                        onChange={handleChange}
                                    >
                                        {seasons.map((season) => (
                                            <MenuItem key={season} value={season}>
                                                {season}
                                            </MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>

                                <Grid item xs={12}>
                                    <Button
                                        type="submit"
                                        variant="contained"
                                        size="large"
                                        fullWidth
                                        startIcon={isEditMode ? <EditIcon /> : <PersonAddIcon />}
                                        className="glow-green"
                                        sx={{
                                            mt: 2,
                                            py: 1.5,
                                            fontSize: '1.1rem',
                                            backgroundColor: '#4CAF50',
                                            '&:hover': {
                                                backgroundColor: '#45a049',
                                                boxShadow: '0 0 20px rgba(76, 175, 80, 0.5)',
                                            },
                                        }}
                                    >
                                        {isEditMode ? 'Update Farmer' : 'Register Farmer'}
                                    </Button>
                                </Grid>
                            </Grid>
                        </form>
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
}

export default FarmerRegistration;
