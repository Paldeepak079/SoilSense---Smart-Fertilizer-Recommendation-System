# SoilSense - Smart Fertilizer Recommendation System

![SoilSense Logo](logo.png)

A comprehensive **Smart Fertilizer Recommendation Software System** that integrates IoT hardware sensors, supports multiple data input methods, generates official-style Soil Health Cards, and provides machine-learning-based fertilizer recommendations optimized for Indian agriculture.

---

## 🌟 Features

### 🔌 IoT Hardware Integration
- **Real-time data collection** from ESP32 microcontroller + sensors
- Supports soil moisture, pH, EC (Electrical Conductivity), and temperature sensors
- Automatic device registration and farmer linkage
- JSON-based data ingestion via REST API

### 📊 Multiple Data Input Methods
1. **Live IoT Sensors** - Automatic data capture from ESP32 devices
2. **Manual Form Entry** - Web-based form for manual soil parameter input
3. **File Upload** - Supports CSV, Excel (.xlsx/.xls), PDF, Word (.docx), and Images (JPG/PNG) with automatic OCR

### 🤖 Machine Learning Recommendations
- **Random Forest Regressor** for nutrient requirement prediction
- Trained on agricultural reference data for 10+ crops and 3 seasons
- Predicts optimal Nitrogen, Phosphorus, and Potassium requirements (kg/ha)
- Intelligent fertilizer mapping to real products: Urea, DAP, MOP, NPK blends
- **Cost optimization** with Indian market prices (₹)
- Application timing guidance (basal + top dressing schedule)

### 📜 Official Soil Health Card Generation
- **Government-style layout** with unique card ID
- **Multi-format downloads:**
  - PDF (with logo, formatted tables, color-coded results)
  - Excel (.xlsx) with professional styling
  - CSV and JSON for data integration
- Automatic nutrient status classification (Low/Medium/High)
- pH and EC status indicators

### 🎨 Modern Dark-Themed UI
- Responsive React frontend with Material-UI
- **Black and gray color palette** with green agriculture theme accents
- Mobile-friendly design
- Intuitive farmer registration and data entry workflows

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python 3.8+) |
| **Database** | PostgreSQL |
| **ML/AI** | scikit-learn, pandas, numpy |
| **Frontend** | React 18, Material-UI |
| **File Processing** | openpyxl, PyPDF2, python-docx, Pillow, pytesseract |
| **Report Generation** | ReportLab (PDF), openpyxl (Excel) |
| **API Communication** | Axios |

---

## 📁 Project Structure

```
SoilSense/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── farmer.py           # Farmer CRUD APIs
│   │   ├── soil_data.py        # Soil data ingestion APIs
│   │   ├── recommendations.py  # ML recommendation API
│   │   └── soil_health_card.py # Health card generation API
│   ├── ml/
│   │   ├── train_model.py      # Model training script
│   │   ├── inference.py        # ML prediction engine
│   │   └── fertilizer_engine.py # Fertilizer recommendation logic
│   └── services/
│       ├── iot_validator.py    # ESP32 data validation
│       ├── file_parser.py      # Multi-format file parser
│       ├── pdf_generator.py    # PDF Health Card generator
│       ├── excel_generator.py  # Excel export
│       └── csv_json_generator.py # CSV/JSON export
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React app
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── FarmerRegistration.jsx
│   │   │   ├── SoilDataEntry.jsx
│   │   │   └── RecommendationView.jsx
│   │   └── index.js
│   ├── package.json
│   └── public/
├── logo.png
├── .env.example
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **PostgreSQL 12+**
- **Tesseract OCR** (for image uploads)

### 1. Clone Repository

```bash
cd "c:/Users/bhauk/Documents/hackathon/Re-Gen &Quasa4.0/SoilSense"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy ..\.env.example .env
# Edit .env and configure DATABASE_URL
```

**Configure PostgreSQL:**
```sql
-- Create database
CREATE DATABASE soilsense;

-- Database URL format in .env:
-- DATABASE_URL=postgresql://username:password@localhost:5432/soilsense
```

**Train ML Model:**
```bash
python -m ml.train_model
```

**Run Backend Server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Backend will be available at: **http://localhost:8080**  
API Documentation: **http://localhost:8080/docs**

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Run development server
npm start
```

Frontend will be available at: **http://localhost:3000**  
*(If port 3000 is busy, React will automatically use port 3001)*

---

## 📡 IoT Hardware Integration

### ESP32 Data Format

Your ESP32 device should send JSON data to:  
`http://YOUR_SERVER_IP:8080/api/soil-data/iot`

**JSON Payload:**
```json
{
  "device_id": "ESP32_001",
  "soil_moisture": 32.5,
  "soil_ph": 6.8,
  "soil_ec": 1.4,
  "temperature": 29.0,
  "timestamp": "2025-12-23 14:30:00",
  "nitrogen": 25.0,
  "phosphorus": 18.0,
  "potassium": 22.0
}
```

**Register Device First:**
```http
POST /api/devices/register
{
  "device_id": "ESP32_001",
  "name": "Field Sensor 1",
  "farmer_id": 1,
  "location": "Main Field, Village XYZ"
}
```

---

## 📖 Usage Workflow

### Step 1: Register Farmer
- Navigate to **"Register New Farmer"**
- Fill in farmer details (name, mobile, address, crop, season, field area)
- Submit

### Step 2: Input Soil Data

Choose one of three methods:

**A. Manual Entry**
- Select farmer
- Enter N, P, K, pH, EC, moisture values manually
- Submit

**B. IoT Sensors** (if ESP32 is configured)
- Data automatically captured when sensors send readings
- View real-time status in Dashboard

**C. File Upload**
- Upload CSV/Excel/PDF/Word/Image file containing soil test report
- System automatically extracts N, P, K, pH, EC values
- Review and confirm

### Step 3: View Recommendations
- System automatically:
  - Runs ML model to predict nutrient requirements
  - Maps to actual fertilizers (Urea, DAP, MOP)
  - Calculates quantities per hectare and per acre
  - Estimates costs in ₹ (INR)
  - Generates Soil Health Card

### Step 4: Download Reports
- **PDF** - Official Soil Health Card with government-style layout
- **Excel** - Formatted spreadsheet
- **CSV** - Raw data export
- **JSON** - Machine-readable format

---

## 🧪 API Endpoints

### Farmers
- `POST /api/farmers` - Register farmer
- `GET /api/farmers/{id}` - Get farmer details
- `GET /api/farmers` - List all farmers

### Soil Data
- `POST /api/soil-data/iot` - IoT sensor data ingestion
- `POST /api/soil-data/manual` - Manual entry
- `POST /api/soil-data/upload/{farmer_id}` - File upload
- `GET /api/soil-data/{id}` - Get soil data record

### Recommendations
- `POST /api/recommendations/generate` - Generate recommendation
- `GET /api/recommendations/{id}` - Get recommendation details

### Soil Health Card
- `POST /api/soil-health-card/generate` - Generate card
- `GET /api/soil-health-card/{card_id}/download/pdf` - Download PDF
- `GET /api/soil-health-card/{card_id}/download/excel` - Download Excel
- `GET /api/soil-health-card/{card_id}/download/csv` - Download CSV
- `GET /api/soil-health-card/{card_id}/download/json` - Download JSON

Full API documentation available at: `http://localhost:8080/docs`

---

## 🌾 Supported Crops

The ML model is trained on:
- Rice, Wheat, Maize
- Cotton, Sugarcane
- Potato, Tomato, Onion
- Soybean, Groundnut

### Seasons
- **Kharif** (Monsoon: June-October)
- **Rabi** (Winter: October-March)
- **Zaid** (Summer: March-June)

---

## 💰 Fertilizer Products & Pricing

| Fertilizer | N% | P% | K% | Price (₹/kg) |
|------------|----|----|-----------|
| **Urea** | 46 | 0 | 0 | 6 |
| **DAP** | 18 | 46 | 0 | 27 |
| **MOP** | 0 | 0 | 60 | 17 |
| **NPK 17-17-17** | 17 | 17 | 17 | 20 |
| **NPK 14-35-14** | 14 | 35 | 14 | 25 |

*Prices are indicative and based on Indian market averages.*

---

## 🔒 Security Notes

- Change `JWT_SECRET` in `.env` before production deployment
- Use strong PostgreSQL passwords
- Enable HTTPS for production
- Sanitize all file uploads
- Validate ESP32 device_id before accepting data

---

## 🚧 Future Enhancements

- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] User authentication & role-based access
- [ ] Historical data analytics and trends
- [ ] Weather integration for irrigation recommendations
- [ ] Mobile app (Android/iOS)
- [ ] SMS/WhatsApp notifications for farmers
- [ ] Integration with Government Soil Health Card databases

---

## 🤝 Contributing

This is a hackathon project built for **Re-Gen & Quasa 4.0**. Contributions, issues, and feature requests are welcome!

---

## 📄 License

MIT License - feel free to use for agricultural innovation!

---

## 👨‍💻 Author

Built with ❤️ for Indian farmers  
**Project:** SoilSense - Smart Fertilizer Recommendation System  
**Event:** Re-Gen & Quasa 4.0 Hackathon

---

## 📞 Support

For issues or questions:
- Check API documentation at `/docs`
- Review this README
- Open an issue on GitHub

🌱 **Happy Farming!** 🚜
