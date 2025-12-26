# QUICK START GUIDE - SoilSense

## 🚨 Prerequisites Checklist

Before running, make sure you have:

- [ ] **Python 3.8+** installed (`python --version`)
- [ ] **Node.js 16+** installed (`node --version`)
- [ ] **PostgreSQL** installed and running
- [ ] PostgreSQL database created: `CREATE DATABASE soilsense;`

---

## 🚀 Easiest Way to Start (Windows)

### Option 1: Use Startup Scripts (Recommended)

**Terminal 1 - Backend:**
```powershell
cd "c:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense"
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
cd "c:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense"
.\start-frontend.ps1
```

### Option 2: Manual Setup

**Backend Setup (First Time Only):**
```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy ..\.env.example .env

# IMPORTANT: Edit .env and set DATABASE_URL
# Example: DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/soilsense

# Train ML model
python -m ml.train_model
```

**Start Backend:**
```powershell
cd backend
.\venv\Scripts\Activate
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

**Frontend Setup (First Time Only):**
```powershell
cd frontend
npm install
```

**Start Frontend:**
```powershell
cd frontend
npm start
```

---

## 🌐 Access Points

Once running:
- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **API Documentation:** http://localhost:8080/docs

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Python not found"
**Solution:** Install Python from python.org or Microsoft Store

### Issue 2: "Node/npm not found"
**Solution:** Install Node.js from nodejs.org

### Issue 3: "PostgreSQL connection error"
**Solutions:**
1. Make sure PostgreSQL is running (check Services)
2. Create database: `CREATE DATABASE soilsense;`
3. Update `backend/.env` with correct DATABASE_URL
4. Format: `postgresql://username:password@localhost:5432/soilsense`

### Issue 4: "Port 8080 already in use"
**Solution:** Change port in `backend/.env` to 8081 or 8082

### Issue 5: "Port 3000 already in use"
**Solution:** React will automatically offer to use port 3001. Type 'Y' to accept.

### Issue 6: "ModuleNotFoundError in Python"
**Solution:**
```powershell
cd backend
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### Issue 7: "npm ERR!"
**Solution:**
```powershell
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

---

## 🧪 Quick Test (Without Full Setup)

If you just want to see the API documentation:

```powershell
cd backend
pip install fastapi uvicorn
uvicorn main:app --port 8080
```

Then visit: http://localhost:8080/docs

---

## 📞 Still Having Issues?

1. Check what error message you're getting
2. Make sure all prerequisites are installed
3. Try running each command step by step
4. Check if ports 8080 and 3000 are available

**Database Not Set Up?** The backend will fail without PostgreSQL. You can:
- Install PostgreSQL from postgresql.org
- Or use SQLite temporarily (requires code changes)
