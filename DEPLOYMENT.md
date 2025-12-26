# SoilSense Production Deployment

## Quick Deployment Steps

### 1. Commit and Push to GitHub

Using GitHub Desktop:
1. Open GitHub Desktop
2. Review all changes
3. Commit message: "Add deployment configuration"
4. Click "Commit to main"
5. Click "Push origin"

### 2. Deploy Backend (Render.com - Recommended)

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New +" → "Web Service"
3. Select your SoilSense repository
4. Configure:
   - **Name**: `soilsense-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables:
   ```
   ENVIRONMENT=production
   DATABASE_URL=sqlite:///./soilsense.db
   ALLOWED_ORIGINS=https://your-app.netlify.app
   JWT_SECRET=your-secret-key-here
   RATE_LIMIT_ENABLED=true
   LOG_LEVEL=INFO
   ```

6. Click "Create Web Service"
7. **Copy your backend URL** (e.g., `https://soilsense-backend.onrender.com`)

### 3. Deploy Frontend (Netlify)

1. Open Netlify Dashboard
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub" and select your repository
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

5. Click "Show advanced" → "New variable"
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL from step 2 (e.g., `https://soilsense-backend.onrender.com`)

6. Click "Deploy site"

### 4. Update Backend CORS

After getting your Netlify URL:
1. Go back to Render dashboard
2. Update `ALLOWED_ORIGINS` environment variable with your Netlify URL
3. Save and redeploy

### 5. Test Your Live Application! 🎉

Visit your Netlify URL and test:
- ✅ Register a farmer
- ✅ Submit soil data
- ✅ Generate recommendations
- ✅ Download reports

---

## Alternative: Railway Backend Deployment

If you prefer Railway.app:
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add same environment variables
5. Copy your Railway URL

---

## Troubleshooting

**Frontend can't reach backend?**
- Check `REACT_APP_API_URL` is set correctly in Netlify
- Verify CORS settings in backend include your Netlify URL

**Backend errors?**
- Check logs on Render/Railway
- Verify all environment variables are set

---

For detailed instructions, see [deployment_plan.md](file:///C:/Users/bhauk/.gemini/antigravity/brain/cb1987ad-5d3b-478f-bfb1-e88c38a403fe/deployment_plan.md)
