# PostgreSQL Installation Guide for Windows

## 📥 Step 1: Download PostgreSQL

1. **Visit:** https://www.postgresql.org/download/windows/
2. **Click:** "Download the installer" (from EDB)
3. **Select:** Latest version for Windows x86-64
4. **Download:** The `.exe` file (approximately 350MB)

## 🔧 Step 2: Install PostgreSQL

1. **Run the installer** (double-click the downloaded .exe file)

2. **Installation Directory:** 
   - Keep default: `C:\Program Files\PostgreSQL\16` (or latest version)

3. **Select Components:** Check ALL:
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4 (Database management tool)
   - ✅ Stack Builder
   - ✅ Command Line Tools

4. **Data Directory:**
   - Keep default: `C:\Program Files\PostgreSQL\16\data`

5. **Set Password:** 
   - **IMPORTANT:** Remember this password! You'll need it later.
   - Example: `postgres123` (or create your own secure password)

6. **Port:**
   - Keep default: `5432`

7. **Locale:**
   - Keep default (usually "C")

8. **Complete Installation** (takes 5-10 minutes)

## ✅ Step 3: Verify Installation

1. **Open Command Prompt** and run:
   ```cmd
   psql --version
   ```
   You should see: `psql (PostgreSQL) 16.x`

2. **Or** open **pgAdmin 4** from Start Menu

## 🗄️ Step 4: Create Database for SoilSense

**Option A: Using pgAdmin 4 (GUI)**
1. Open pgAdmin 4 from Start Menu
2. Enter your master password (if prompted)
3. Right-click "Databases" → "Create" → "Database"
4. Database name: `soilsense`
5. Click "Save"

**Option B: Using Command Line**
1. Open Command Prompt
2. Run:
   ```cmd
   psql -U postgres
   ```
3. Enter your password when prompted
4. Run:
   ```sql
   CREATE DATABASE soilsense;
   ```
5. Type `\q` to exit

## 🔗 Step 5: Update SoilSense Configuration

1. **Navigate to your project:**
   ```cmd
   cd "c:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense\backend"
   ```

2. **Create `.env` file** (if not exists):
   ```cmd
   copy ..\.env.example .env
   ```

3. **Edit `backend\.env`** and update:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/soilsense
   ```
   
   Replace `YOUR_PASSWORD` with the password you set during installation!

## 🎯 Example Configuration

If your PostgreSQL password is `postgres123`:
```env
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/soilsense
```

## ✨ You're Ready!

After completing these steps, you can run:

```powershell
cd "c:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense"
.\start-backend.ps1
```

The backend will automatically:
- Connect to PostgreSQL
- Create all database tables
- Train the ML model
- Start the API server

---

## 🆘 Troubleshooting

### "psql: command not found"
- Add PostgreSQL to PATH:
  - Search "Environment Variables" in Windows
  - Edit System Environment Variables
  - Add: `C:\Program Files\PostgreSQL\16\bin`

### "Connection refused"
- Make sure PostgreSQL service is running:
  - Open Services (services.msc)
  - Find "postgresql-x64-16" (or your version)
  - Start it if stopped

### "Password authentication failed"
- Double-check your password in `backend\.env`
- Username is usually `postgres`

---

## 📞 Quick Help

Once installed, you can check PostgreSQL status:
- **GUI:** Open pgAdmin 4
- **Command Line:** `psql -U postgres -d soilsense`

Need to reset password? Use pgAdmin 4:
1. Right-click "postgres" user
2. Properties → Definition → Password
