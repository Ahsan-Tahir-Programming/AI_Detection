# Free Hosting & Deployment Guide

## Project Status ✓

Your project is now clean and ready for deployment:

- ✅ Pydantic models integrated
- ✅ Type-safe API with OpenAPI docs
- ✅ Dark/light theme implemented
- ✅ Download functionality working
- ✅ Pagination implemented
- ✅ Classes configuration externalized
- ✅ Unnecessary files removed (.DS_Store, logs, etc.)
- ✅ .gitignore properly configured

---

## Frontend Hosting Options

### 1. **Vercel** (Recommended - Best for React)

**Cost:** FREE (Hobby plan)
**Why:** Perfect for React/Vite apps, automatic deployments from GitHub

#### Setup:

1. Push code to GitHub: `git push origin main`
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Configure build settings:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Root Directory:** `frontend`
6. Set environment variables:
   - `VITE_API_URL=https://your-api.onrender.com` (or your backend URL)
7. Deploy! 🚀

**Cost:** $0/month (unlimited projects, domains at vercel.app)

---

### 2. **Netlify**

**Cost:** FREE (Starter plan)

#### Setup:

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Select GitHub and authorize
4. Choose your repository
5. Build settings:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
6. Set environment variables in Site settings → Build & deploy → Environment
7. Deploy!

**Cost:** $0/month

---

### 3. **GitHub Pages** (If API is separate)

**Cost:** FREE
**Setup:** Modify `vite.config.ts` for base path, then use GitHub Actions

---

## Backend Hosting Options

### 1. **Render** (Recommended - Best for Python/FastAPI)

**Cost:** FREE (until March 18, 2025) / $7/month after
**Pros:** Simple deployment, automatic deploys from GitHub, generous free tier

#### Setup:

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** `ai-detection-api`
   - **Environment:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Region:** Choose closest to you
6. Set environment variables:
   - `DOCKER_ENV=false` (if using local environment)
7. Deploy!

**Free Plan:**

- 750 hours/month (that's 31 days running 24/7!)
- Spins down after 15 minutes of inactivity
- 0.5 CPU, 512 MB RAM

**Cost:** $0/month on free tier, $7/month for paid

---

### 2. **Railway** (Alternative - Good for Python)

**Cost:** FREE ($5 credits/month, usually enough for hobby projects)

#### Setup:

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project → Deploy from GitHub
4. Select your repository
5. Railway auto-detects it's Python
6. Configure:
   - Set environment variables
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
7. Deploy!

**Cost:** $0 with credits (~$5/month free credits)

---

### 3. **Heroku** (Deprecated free tier as of Nov 2022)

**Cost:** Paid only ($7/month minimum)
**Not recommended for free deployment**

---

### 4. **Azure App Service** (Alternative)

**Cost:** FREE tier (limited)

- 1 GB memory
- Shared compute
- Daily limits

#### Setup:

1. Create Azure account
2. Deploy via VS Code extension or GitHub Actions
3. Limited resources but completely free

---

## Recommended Combination (100% Free)

### **Frontend: Vercel** + **Backend: Render**

```
┌─────────────────────────────────────────┐
│         Your GitHub Repository          │
│  ┌──────────────────────────────────┐  │
│  │ frontend/  (React + Vite)        │  │
│  │ app/       (FastAPI)             │  │
│  │ docker-compose.yml               │  │
│  │ requirements.txt                 │  │
│  └──────────────────────────────────┘  │
└────────┬──────────────────────────┬─────┘
         │                          │
    receives push                receives push
         │                          │
         ▼                          ▼
    ┌────────────┐           ┌──────────────┐
    │  Vercel    │           │   Render     │
    │ (Frontend) │           │  (Backend)   │
    │   FREE     │           │    FREE      │
    │ ai-detect  │           │ ai-detection-│
    │ .vercel.app│           │  api.onrender│
    │            │           │  .com        │
    └────────────┘           └──────────────┘
         ▲                          ▲
         │                          │
         └──────────────┬───────────┘
                        │
                    (API calls)
```

**Total Cost:** $0/month ✓

---

## Pre-Deployment Checklist

Before pushing to GitHub:

### Backend

- [ ] Update `requirements.txt` with all dependencies
- [ ] Set `DEBUG=False` in production
- [ ] Add CORS configuration for your frontend domain
- [ ] Database migrations are ready
- [ ] Environment variables documented (see .env.example)
- [ ] No hardcoded API keys

### Frontend

- [ ] `VITE_API_URL` environment variable set to backend URL
- [ ] Build passes: `npm run build`
- [ ] No console errors in production build
- [ ] All API endpoints tested
- [ ] Images/assets load correctly

### Project Setup

- [ ] `.gitignore` properly configured (✓ Done)
- [ ] Sensitive files not committed (✓ Done)
- [ ] README.md with setup instructions
- [ ] `.env.example` file created

---

## Setup Instructions for Deployment

### Create `.env.example` File

Backend root directory needs this file to show what env vars are needed:

```env
# Backend Environment Variables
DEBUG=False
DOCKER_ENV=False
DATABASE_URL=sqlite:///app/database/detections.db

# Frontend should know the API URL
# (This is set via Vercel environment variable)
```

Create this file:

```bash
# In project root
echo "# Example environment variables
DEBUG=False
DOCKER_ENV=False
DATABASE_URL=sqlite:///app/database/detections.db" > .env.example
```

---

## Git Setup Before Deployment

```bash
# Initialize git if not done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Detection System ready for deployment"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/Ai_Detection.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
cd /path/to/project
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com)
2. New Web Service from GitHub
3. Use this **Start Command:**
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Wait for deployment (2-5 minutes)
5. Copy the URL: `https://your-api-name.onrender.com`

### Step 3: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Root Directory: `frontend`
4. Build Command: `npm run build`
5. Add environment variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-api-name.onrender.com`
6. Deploy!

### Step 4: Update CORS if needed

In `app/main.py`, update the allowed origin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition"]
)
```

---

## Database & File Storage

### SQLite Database

- Local SQLite (`detections.db`) works fine on Render
- Data persists between deployments
- Limited to ~100GB, very sufficient for this project

### Uploaded Images

- Stored in `app/download/` directory
- On Render: Ephemeral storage (deleted on redeploy)
- **Solution:** Use AWS S3/Cloudinary for permanent storage (free tier available)

#### For Production Image Storage:

1. **Cloudinary** (FREE - 25 MB storage):
   - Perfect for demo/hobby projects
   - Fast CDN delivery
   - Get API key at [cloudinary.com](https://cloudinary.com)

2. **AWS S3** (FREE - 1 year free tier):
   - 5 GB free storage
   - More durable long-term solution

---

## Custom Domain (Optional)

### Vercel

Add custom domain in Vercel dashboard → Settings → Domains

### Render

Free `.onrender.com` subdomain included
Custom domain: $10/month ($0 on free tier)

---

## Monitoring & Logs

### Vercel

- Dashboard shows deployments
- Logs visible in real-time
- Free tier includes basic analytics

### Render

- Real-time logs in dashboard
- Monitor CPU/Memory usage
- Email alerts available

---

## Cost Summary

| Service           | Free Plan    | Notes                         |
| ----------------- | ------------ | ----------------------------- |
| Vercel (Frontend) | ✅ Yes       | Unlimited projects            |
| Render (Backend)  | ✅ Yes       | 750 hrs/month (24/7 coverage) |
| GitHub            | ✅ Yes       | Unlimited public repos        |
| **Total**         | **$0/month** | ✓ Completely free             |

---

## Troubleshooting

### Issue: Frontend can't reach backend

**Solution:** Set `VITE_API_URL` environment variable in Vercel

### Issue: Render deployment fails

**Solution:** Check `requirements.txt` includes all imports (especially `ultralytics`, `torch`)

### Issue: Images not persisting

**Solution:** Use cloud storage (Cloudinary/S3) instead of local filesystem

### Issue: "502 Bad Gateway"

**Solution:** Backend may be sleeping on free tier. Add keep-alive service

---

## Next Steps

1. ✅ Clean project (Done)
2. → Create `.env.example` file
3. → Push to GitHub
4. → Deploy on Render (backend)
5. → Deploy on Vercel (frontend)
6. → Test both environments
7. → Share your deployed links!

---

## Resources

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
