import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
    Alert,
    LinearProgress,
    Tabs,
    Tab,
    MenuItem,
    Select
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SaveIcon from '@mui/icons-material/Save';
import axios from 'axios';
import { LanguageContext } from '../App';
import { LANGUAGES, getText } from '../utils/translations';

function SoilDataEntry() {
    const navigate = useNavigate();
    const { farmerId } = useParams();
    const [farmer, setFarmer] = useState(null);
    const [activeTab, setActiveTab] = useState(0);
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const { language, setLanguage } = useContext(LanguageContext);

    // Validation State
    const [validationErrors, setValidationErrors] = useState({});

    const [manualData, setManualData] = useState({
        nitrogen: '',
        phosphorus: '',
        potassium: '',
        ph: '',
        ec: '',
        moisture: '',
        organic_carbon: '',
    });

    useEffect(() => {
        fetchFarmer();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [farmerId]);

    const fetchFarmer = async () => {
        try {
            const response = await axios.get(`/api/farmers/${farmerId}`);
            setFarmer(response.data);
        } catch (err) {
            setError(getText('failed_load_farmer', language) || 'Failed to load farmer details');
        }
    };

    const validateField = (name, value) => {
        let msg = null;
        const val = parseFloat(value);
        if (isNaN(val)) return null; // Don't validate empty/incomplete

        switch (name) {
            case 'ph':
                if (val < 3.5 || val > 9.0) msg = "pH must be between 3.5 and 9.0";
                break;
            case 'ec':
                if (val < 0 || val > 4.0) msg = "EC must be between 0 and 4.0 dS/m";
                break;
            case 'moisture':
                if (val < 0 || val > 100) msg = "Moisture must be between 0% and 100%";
                break;
            default:
                break;
        }
        return msg;
    };

    const handleManualChange = (e) => {
        const { name, value } = e.target;
        setManualData({
            ...manualData,
            [name]: value,
        });

        // Real-time validation
        const errorMsg = validateField(name, value);
        setValidationErrors(prev => ({
            ...prev,
            [name]: errorMsg
        }));
    };

    const handleManualSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Block if errors exist
        const hasErrors = Object.values(validationErrors).some(x => x !== null);
        if (hasErrors) {
            setError("Please correct validaton errors before submitting.");
            return;
        }

        try {
            const response = await axios.post('/api/soil-data/manual', {
                farmer_id: parseInt(farmerId),
                nitrogen: parseFloat(manualData.nitrogen) || null,
                phosphorus: parseFloat(manualData.phosphorus) || null,
                potassium: parseFloat(manualData.potassium) || null,
                ph: parseFloat(manualData.ph) || null,
                ec: parseFloat(manualData.ec) || null,
                moisture: parseFloat(manualData.moisture) || null,
                organic_carbon: parseFloat(manualData.organic_carbon) || null,
            });

            setSuccess(true);
            setTimeout(() => {
                navigate(`/recommendation/${farmerId}/${response.data.id}`);
            }, 1500);
        } catch (err) {
            setError(err.response?.data?.detail || getText('failed_submit', language) || 'Failed to submit soil data');
        }
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            await handleFileUpload(e.dataTransfer.files[0]);
        }
    };

    const handleFileSelect = async (e) => {
        if (e.target.files && e.target.files[0]) {
            await handleFileUpload(e.target.files[0]);
        }
    };

    const handleFileUpload = async (file) => {
        setUploading(true);
        setUploadProgress(0);
        setError('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`/api/soil-data/upload/${farmerId}`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(progress);
                },
            });

            setSuccess(true);
            setTimeout(() => {
                navigate(`/recommendation/${farmerId}/${response.data.id}`);
            }, 1500);
        } catch (err) {
            setError(err.response?.data?.detail || getText('failed_upload', language) || 'Failed to upload file.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <Box sx={{ minHeight: '100vh', backgroundColor: '#000000' }}>
            <AppBar position="sticky" elevation={0} sx={{ top: 0, zIndex: 1100, backgroundColor: 'rgba(0, 0, 0, 0.2)', backdropFilter: 'blur(20px)', borderBottom: 'none' }}>
                <Toolbar>
                    <img
                        src="/logo.png"
                        alt="SoilSense Logo"
                        style={{
                            height: '60px',
                            marginRight: '16px',
                        }}
                    />
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{
                            flexGrow: 1,
                            fontWeight: 600,
                            color: '#4CAF50',
                            textShadow: '0 0 10px rgba(76, 175, 80, 0.5)'
                        }}
                    >
                        Soilsense - {getText('soil_data_entry', language) || 'Soil Data Entry'}
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
                    <Button
                        color="inherit"
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/')}
                    >
                        {getText('back_dashboard', language) || 'Dashboard'}
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4, pb: 4 }}>
                {farmer && (
                    <Card className="premium-card" sx={{ mb: 3 }}>
                        <CardContent>
                            <Typography variant="h6" className="text-glow" sx={{ color: '#4CAF50' }}>
                                {getText('farmer', language) || 'Farmer'}: {farmer.name}
                            </Typography>
                            <Typography variant="body2" sx={{ color: '#e0e0e0' }}>
                                {farmer.village}, {farmer.district} | {getText('crop', language) || 'Crop'}: {farmer.crop_name} ({farmer.crop_season})
                            </Typography>
                        </CardContent>
                    </Card>
                )}

                {error && (
                    <Alert severity="error" sx={{ mb: 2, backgroundColor: 'rgba(211, 47, 47, 0.1)' }}>
                        {typeof error === 'string' ? error : JSON.stringify(error)}
                    </Alert>
                )}

                {success && (
                    <Alert severity="success" sx={{ mb: 2, backgroundColor: 'rgba(76, 175, 80, 0.1)' }}>
                        {getText('data_submitted', language) || 'Soil data submitted successfully! Generating recommendations...'}
                    </Alert>
                )}

                <Card className="premium-card">
                    <CardContent>
                        <Tabs
                            value={activeTab}
                            onChange={(e, newValue) => setActiveTab(newValue)}
                            sx={{ borderBottom: 1, borderColor: 'rgba(76, 175, 80, 0.3)', mb: 3, '& .MuiTab-root': { color: '#e0e0e0' }, '& .Mui-selected': { color: '#4CAF50' } }}
                        >
                            <Tab label={getText('manual_entry', language) || 'Manual Entry'} />
                            <Tab label={getText('upload_file', language) || 'Upload File'} />
                        </Tabs>

                        {activeTab === 0 && (
                            <form onSubmit={handleManualSubmit}>
                                <Grid container spacing={3}>
                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            label="Nitrogen (mg/kg)"
                                            name="nitrogen"
                                            type="number"
                                            value={manualData.nitrogen}
                                            onChange={handleManualChange}
                                            inputProps={{ min: 0, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            label="Phosphorus (mg/kg)"
                                            name="phosphorus"
                                            type="number"
                                            value={manualData.phosphorus}
                                            onChange={handleManualChange}
                                            inputProps={{ min: 0, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            label="Potassium (mg/kg)"
                                            name="potassium"
                                            type="number"
                                            value={manualData.potassium}
                                            onChange={handleManualChange}
                                            inputProps={{ min: 0, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            required
                                            label="pH"
                                            name="ph"
                                            type="number"
                                            value={manualData.ph}
                                            onChange={handleManualChange}
                                            error={!!validationErrors.ph}
                                            helperText={validationErrors.ph}
                                            inputProps={{ min: 0, max: 14, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            label="EC (dS/m)"
                                            name="ec"
                                            type="number"
                                            value={manualData.ec}
                                            onChange={handleManualChange}
                                            error={!!validationErrors.ec}
                                            helperText={validationErrors.ec}
                                            inputProps={{ min: 0, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12} md={4}>
                                        <TextField
                                            fullWidth
                                            label="Moisture (%)"
                                            name="moisture"
                                            type="number"
                                            value={manualData.moisture}
                                            onChange={handleManualChange}
                                            error={!!validationErrors.moisture}
                                            helperText={validationErrors.moisture}
                                            inputProps={{ min: 0, max: 100, step: 0.1 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12}>
                                        <TextField
                                            fullWidth
                                            label="Organic Carbon (%)"
                                            name="organic_carbon"
                                            type="number"
                                            value={manualData.organic_carbon}
                                            onChange={handleManualChange}
                                            inputProps={{ min: 0, step: 0.01 }}
                                        />
                                    </Grid>

                                    <Grid item xs={12}>
                                        <Button
                                            type="submit"
                                            variant="contained"
                                            size="large"
                                            fullWidth
                                            startIcon={<SaveIcon />}
                                            disabled={Object.values(validationErrors).some(x => x !== null)}
                                            className="glow-green"
                                            sx={{
                                                mt: 2,
                                                py: 1.5,
                                                backgroundColor: '#4CAF50',
                                                '&:hover': {
                                                    backgroundColor: '#45a049',
                                                    boxShadow: '0 0 20px rgba(76, 175, 80, 0.5)',
                                                },
                                            }}
                                        >
                                            {getText('submit_generate', language) || 'Submit & Generate Recommendations'}
                                        </Button>
                                    </Grid>
                                </Grid>
                            </form>
                        )}

                        {activeTab === 1 && (
                            <Box>
                                <Box
                                    onDragEnter={handleDrag}
                                    onDragLeave={handleDrag}
                                    onDragOver={handleDrag}
                                    onDrop={handleDrop}
                                    className={dragActive ? "glow-green-strong border-glow" : "border-glow"}
                                    sx={{
                                        p: 6,
                                        textAlign: 'center',
                                        borderRadius: 2,
                                        backgroundColor: dragActive ? 'rgba(76, 175, 80, 0.1)' : '#000000',
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease',
                                        '&:hover': {
                                            borderColor: 'rgba(76, 175, 80, 0.6)',
                                            backgroundColor: 'rgba(76, 175, 80, 0.05)',
                                        },
                                    }}
                                    onClick={() => document.getElementById('file-input').click()}
                                >
                                    <CloudUploadIcon sx={{ fontSize: 64, color: '#4CAF50', mb: 2 }} />
                                    <Typography variant="h6" className="text-glow" sx={{ mb: 1 }}>
                                        {dragActive ? getText('drop_file', language) : getText('drag_drop', language) || 'Drag & Drop or Click to Upload'}
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: '#e0e0e0', mb: 2 }}>
                                        Supported formats: PDF, Excel (.xlsx, .xls, .csv), Word (.docx), Images (.jpg, .png)
                                    </Typography>
                                    <Typography variant="caption" sx={{ color: '#81C784' }}>
                                        The file should contain soil test report with N, P, K, pH values
                                    </Typography>
                                    <input
                                        id="file-input"
                                        type="file"
                                        accept=".pdf,.xlsx,.xls,.csv,.docx,.jpg,.jpeg,.png"
                                        onChange={handleFileSelect}
                                        style={{ display: 'none' }}
                                    />
                                </Box>

                                {uploading && (
                                    <Box sx={{ mt: 3 }}>
                                        <LinearProgress
                                            variant="determinate"
                                            value={uploadProgress}
                                            sx={{
                                                height: 8,
                                                borderRadius: 4,
                                                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                                                '& .MuiLinearProgress-bar': {
                                                    backgroundColor: '#4CAF50',
                                                    boxShadow: '0 0 10px rgba(76, 175, 80, 0.5)',
                                                },
                                            }}
                                        />
                                        <Typography variant="body2" sx={{ mt: 1, textAlign: 'center', color: '#81C784' }}>
                                            {getText('uploading', language) || 'Uploading'}... {uploadProgress}%
                                        </Typography>
                                    </Box>
                                )}
                            </Box>
                        )}
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
}

export default SoilDataEntry;
