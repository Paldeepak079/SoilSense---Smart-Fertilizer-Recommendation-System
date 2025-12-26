# 🚀 Getting SoilSense Running - Step by Step

## ✅ Step 1: Install PostgreSQL (You are here!)

1. **Double-click** the PostgreSQL installer you just downloaded
2. Click **Next** through the welcome screen
3. **Installation Directory:** Keep default → Click **Next**
4. **Select Components:** Make sure ALL are checked:
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4
   - ✅ Stack Builder  
   - ✅ Command Line Tools
   Click **Next**

5. **Data Directory:** Keep default → Click **Next**

6. **⚠️ SUPER IMPORTANT - Password:**
   - You'll see "Password for database superuser (postgres)"
   - **Enter a password you'll remember** (example: `postgres123`)
   - **Write it down!** You'll need it in a few minutes
   - Confirm the password
   - Click **Next**

7. **Port:** Keep `5432` → Click **Next**
8. **Locale:** Keep default → Click **Next**
9. Click **Next** on the summary screen
10. Click **Next** to start installation (takes 5-10 minutes)
11. **Uncheck** "Stack Builder" at the end → Click **Finish**

---

## ✅ Step 2: Create Database

**Open Command Prompt and run:**

```cmd
psql -U postgres
```

When it asks for password, **type the password you just created** (you won't see the characters as you type - that's normal!)

Then type:
```sql
CREATE DATABASE soilsense;
```

You should see: `CREATE DATABASE`

Type:
```sql
\q
```

to exit.

---

## ✅ Step 3: Configure SoilSense

**Open a new Command Prompt/PowerShell** in your project folder:

```powershell
cd "C:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense\backend"
```

**Create the .env file:**
```powershell
copy ..\.env.example .env
```

**Edit the .env file:**
- Open `backend\.env` in any text editor
- Find the line: `DATABASE_URL=postgresql://postgres:password@localhost:5432/soilsense`
- **Replace `password` with YOUR PostgreSQL password**
- Example: `DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/soilsense`
- **Save the file**

---

## ✅ Step 4: Run the Application!

**Open TWO terminal windows:**

### Terminal 1 - Backend:
```powershell
cd "C:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense"
.\start-backend.ps1
```

Wait for it to say: **"Application startup complete"**

### Terminal 2 - Frontend:
```powershell
cd "C:\Users\bhauk\Documents\hackathon\Re-Gen &Quasa4.0\SoilSense"
.\start-frontend.ps1
```

---

## 🎉 Access Your App!

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8080/docs

---

## 🆘 If Something Goes Wrong

**Backend won't start?**
- Check your password in `backend\.env`
- Make sure PostgreSQL is running (check Windows Services)

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Try: `cd frontend` then `npm install` then `npm start`

**Port already in use?**
- React will ask if you want to use port 3001 - say Yes (Y)

---

## 📍 Where You Are Now:

✅ PostgreSQL downloaded  
⏳ **Next:** Run the installer (double-click it!)  
⏳ Create database  
⏳ Configure .env  
⏳ Start the app  

**Just follow the steps above in order!** 🚀
