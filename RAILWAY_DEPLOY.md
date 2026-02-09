# GuardianPDF Railway Deployment Guide

## 🚂 Deploying to Railway (Easiest Option!)

Railway is perfect for GuardianPDF because:
- ✅ Excellent C++ support
- ✅ 8GB RAM on free tier (enough for models)
- ✅ Built-in persistent volumes
- ✅ Easy environment variables
- ✅ Automatic HTTPS
- ✅ $5/month starter plan

---

## Quick Deploy (5 minutes)

### Option 1: GitHub Integration (Recommended)

1. **Go to Railway Dashboard**:
   - Visit https://railway.app
   - Click "Start a New Project"

2. **Deploy from GitHub**:
   - Choose "Deploy from GitHub repo"
   - Select your repository: `aarushdubey/Guardian_PDF`
   - Railway will auto-detect and deploy

3. **Set Environment Variables**:
   Click on your service → Variables tab → Add:
   ```
   NVIDIA_API_KEY=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
   LLM_PROVIDER=nvidia
   NVIDIA_MODEL=meta/llama3-70b-instruct
   ```

4. **Add Volume (for ChromaDB)**:
   - Go to service → Settings → Volumes
   - Create volume
   - Mount path: `/app/chroma_db`
   - Size: 1GB

5. **Deploy!**
   - Railway builds automatically
   - Wait ~3-5 minutes for first build
   - Your app will be live!

### Option 2: Railway CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize
cd /Users/aarushdubey/Downloads/guardian_pdf
railway init

# 4. Link to GitHub repo (optional)
railway link

# 5. Set environment variables
railway variables set NVIDIA_API_KEY=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
railway variables set LLM_PROVIDER=nvidia
railway variables set NVIDIA_MODEL=meta/llama3-70b-instruct

# 6. Deploy
railway up
```

---

## 📝 Configuration Files

I've created:
- ✅ `railway.json` - Railway configuration
- ✅ `railway_build.sh` - Build script for C++ + models

Railway will automatically:
1. Install system dependencies (g++, cmake, poppler)
2. Build C++ module
3. Install Python packages
4. Pre-download AI models
5. Start the server

---

## 🔧 Build Process

**What happens during deployment:**

```
1. Railway detects Python project ✅
2. Runs railway_build.sh:
   - Installs C++ toolchain
   - Compiles PDFShredder module
   - Downloads embedding models
   - Downloads GPT-2 for AI detection
3. Starts app with: python rag_engine/app.py
4. Health check on port 8000
```

**Build time**: ~3-5 minutes (first time), ~1-2 minutes (subsequent)

---

## 🌐 Accessing Your App

After deployment:

1. **Get URL**: Railway generates a URL like `guardianpdf-production.up.railway.app`
2. **Test it**:
   ```bash
   curl https://YOUR-APP.up.railway.app/
   ```

3. **Upload PDF**:
   ```bash
   curl -X POST https://YOUR-APP.up.railway.app/upload_pdf \
     -F "file=@document.pdf"
   ```

---

## 📊 Resource Usage

| Component | RAM | Storage |
|-----------|-----|---------|
| Total Needed | ~1-2GB | ~500MB |
| Railway Free Tier | 8GB | 1GB volume |
| **Status** | ✅ Plenty | ✅ Sufficient |

---

## 💰 Pricing

**Free Tier** (Trial):
- $5 free credit
- All features unlocked
- Perfect for testing/demo

**Starter Plan** ($5/month):
- Recommended for production
- 8GB RAM included
- 100GB egress
- Persistent volumes

---

## ⚙️ Environment Variables to Set

In Railway dashboard, add these:

```bash
# Required
NVIDIA_API_KEY=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
LLM_PROVIDER=nvidia

# Optional
NVIDIA_MODEL=meta/llama3-70b-instruct
CHROMA_PERSIST_DIR=/app/chroma_db
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🐛 Troubleshooting

### Build Fails
- **Check logs** in Railway dashboard → Deployments → View logs
- Common issue: C++ dependencies missing (fixed in railway_build.sh)

### App Crashes on Start
- **Check memory**: Should have at least 1GB
- **Check environment variables**: NVIDIA_API_KEY must be set

### Models Taking Too Long
- Models are pre-downloaded during build (railway_build.sh)
- First startup ~30 seconds, subsequent ~5 seconds

---

## ✅ Deployment Checklist

- [x] Railway account created
- [x] GitHub repo connected
- [ ] Environment variables set
- [ ] Volume created for ChromaDB
- [ ] First deployment successful
- [ ] Test endpoints working
- [ ] Add URL to resume!

---

## 🎯 After Deployment

**Add to your resume**:
```
GuardianPDF - Live Demo: https://guardianpdf.up.railway.app
3-tier PDF assistant with C++ performance, NVIDIA AI, and security auditing
```

**Share it**:
- Add to LinkedIn projects
- Include in Master's applications
- Demo for interviews

---

## 🚀 Deploy Now!

**Fastest way**:
1. Go to https://railway.app
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select: `aarushdubey/Guardian_PDF`
5. Add environment variables
6. Done! ✅

**Your app will be live in ~5 minutes!**

---

Need help? Railway has excellent docs: https://docs.railway.app
