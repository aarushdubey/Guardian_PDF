# GuardianPDF Deployment Guide

## 🚀 Deployment Options Comparison

| Platform | Difficulty | Cost | Best For | C++ Support |
|----------|-----------|------|----------|-------------|
| **Railway** ⭐ | Easy | $5/mo | Production | ✅ Excellent |
| **Fly.io** | Easy | Free tier | Global edge | ✅ Good (Docker) |
| **Render** | Medium | $7/mo+ | Simple apps | ⚠️ Needs Docker |
| **AWS/GCP** | Hard | Variable | Enterprise | ✅ Excellent |
| **Docker (Self-host)** | Easy | Server cost | Full control | ✅ Perfect |

---

## Option 1: Railway (Recommended) ⭐

**Best for GuardianPDF** - handles C++, good pricing, easy setup

### Steps:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   cd /Users/aarushdubey/Downloads/guardian_pdf
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables** in Railway dashboard:
   ```
   NVIDIA_API_KEY=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
   LLM_PROVIDER=nvidia
   ```

4. **Add Volume** (for ChromaDB):
   - Go to Railway dashboard → Your service → Settings → Volumes
   - Mount path: `/app/chroma_db`

**Cost**: ~$5/month

---

## Option 2: Fly.io (Docker-based)

### Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml**:
   ```bash
   fly launch
   ```

3. **Set Secrets**:
   ```bash
   fly secrets set NVIDIA_API_KEY=nvapi-YOUR_KEY
   ```

4. **Deploy**:
   ```bash
   fly deploy
   ```

**Cost**: Free tier available (256MB×3 VMs)

---

## Option 3: Render (with Docker)

### Steps:

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: guardianpdf
       env: docker
       dockerfilePath: ./Dockerfile
       envVars:
         - key: NVIDIA_API_KEY
           sync: false
       disk:
         name: chroma-data
         mountPath: /app/chroma_db
         sizeGB: 1
   ```

2. **Push to GitHub** (already done ✅)

3. **Connect to Render**:
   - Go to render.com → New → Blueprint
   - Connect your GitHub repo
   - Render will auto-deploy

**Cost**: $7/month (Starter plan needed for Docker)

---

## Option 4: Docker (Self-Host/VPS)

**Use the Docker files I just created!**

### Quick Start:

```bash
cd /Users/aarushdubey/Downloads/guardian_pdf

# Build and run
docker-compose up -d

# Check status
docker-compose logs -f

# Access at http://localhost:8000
```

### Deploy to VPS (DigitalOcean, Linode, etc.):

```bash
# On your VPS
git clone https://github.com/aarushdubey/Guardian_PDF.git
cd Guardian_PDF

# Create .env file
echo "NVIDIA_API_KEY=nvapi-YOUR_KEY" > .env

# Deploy
docker-compose up -d
```

**Cost**: $5-10/month for VPS

---

## 🎯 My Recommendation

**For your case (portfolio + learning):**

### Best Choice: **Fly.io** (Free Tier)

**Why:**
1. ✅ Free tier sufficient for demos
2. ✅ Easy Docker deployment (Dockerfile ready)
3. ✅ Global CDN (fast access)
4. ✅ Good for resume/portfolio

### Commands to Deploy:

```bash
# 1. Install Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Initialize (in guardian_pdf directory)
cd /Users/aarushdubey/Downloads/guardian_pdf
fly launch --name guardianpdf

# 4. Set secrets
fly secrets set NVIDIA_API_KEY=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

# 5. Deploy!
fly deploy
```

**Your app will be live at**: `https://guardianpdf.fly.dev`

---

## 📝 Pre-Deployment Checklist

- [x] Docker files created (Dockerfile, docker-compose.yml)
- [x] Code on GitHub
- [x] NVIDIA API key configured
- [ ] Choose platform (Railway/Fly.io/Render)
- [ ] Deploy
- [ ] Test live endpoint
- [ ] Add URL to resume!

---

## 🔒 Security Notes

1. **Never commit .env** with real API keys (already in .gitignore ✅)
2. **Use environment variables** on deployment platform
3. **Enable HTTPS** (all platforms do this automatically)
4. **Consider rate limiting** for production

---

## 📊 Resource Requirements

| Component | RAM | Storage |
|-----------|-----|---------|
| Embedding Model | ~500MB | 200MB |
| GPT-2 (AI Detection) | ~300MB | 150MB |
| FastAPI | ~100MB | - |
| ChromaDB | ~100MB | Variable |
| **Total** | **~1GB** | **500MB+** |

**Minimum**: 1GB RAM, 1GB storage  
**Recommended**: 2GB RAM, 2GB storage

---

Want me to help you deploy to Fly.io right now? It's the easiest option!
