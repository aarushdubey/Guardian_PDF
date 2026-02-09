# GuardianPDF - Render.com Deployment Guide

## 🎯 Quick Start (5 Minutes)

### Step 1: Sign Up with GitHub
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account
4. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Guardian_PDF`
3. Render will auto-detect your Dockerfile ✅

### Step 3: Configure Service
**Name**: `guardianpdf`
**Region**: Singapore (closest to India)
**Branch**: `main`
**Runtime**: Docker
**Plan**: **Free** (select this!)

### Step 4: Add Environment Variables
Click "Advanced" and add these environment variables:

```
LLM_PROVIDER=nvidia
NVIDIA_MODEL=meta/llama3-70b-instruct
CHROMA_PERSIST_DIR=/data/chroma_db
NVIDIA_API_KEY=<your-nvidia-api-key>
```

### Step 5: Add Persistent Disk
1. Scroll to "Disks"
2. Click "Add Disk"
3. **Name**: `chroma-data`
4. **Mount Path**: `/data/chroma_db`
5. **Size**: 1 GB (free tier limit)

### Step 6: Deploy! 🚀
1. Click "Create Web Service"
2. Render will:
   - Clone your repo
   - Build Docker image
   - Deploy to Singapore
   - Give you a live URL

**Deployment time**: ~10-15 minutes

---

## 📊 What You Get (FREE)

✅ **Hosting**: Free forever (with limitations)
✅ **RAM**: 512 MB (enough for your app)
✅ **Storage**: 1 GB persistent disk
✅ **Bandwidth**: 100 GB/month
✅ **SSL**: Free HTTPS certificate
✅ **Auto-deploy**: Updates on every Git push
✅ **Custom domain**: Supported

⚠️ **Free Tier Limitations**:
- Spins down after 15 min of inactivity
- First request after sleep: 30-60 sec cold start
- No always-on guarantee

---

## 🔗 Your Live URL

After deployment: `https://guardianpdf.onrender.com`

**Test the API**:
```bash
# Health check
curl https://guardianpdf.onrender.com/health

# API docs (interactive)
open https://guardianpdf.onrender.com/docs
```

---

## 🛠️ Managing Your App

### View Logs
Dashboard → Your Service → Logs

### Restart Service
Dashboard → Your Service → Manual Deploy → "Clear build cache & deploy"

### Update Environment Variables
Dashboard → Your Service → Environment → Edit

### Scale Up (if needed later)
Dashboard → Your Service → Settings → Change Plan
- **Starter**: $7/month (always-on, 512MB RAM)
- **Standard**: $25/month (2GB RAM)

---

## 🔄 Auto-Deploy on Git Push

Every time you push to `main` branch:
1. Render detects the change
2. Rebuilds Docker image
3. Deploys automatically
4. Zero downtime!

```bash
git add .
git commit -m "Update feature"
git push origin main
# Render auto-deploys!
```

---

## 🐛 Troubleshooting

### Build Fails
- Check build logs in dashboard
- Ensure Dockerfile is in root
- Verify all files are committed

### App Crashes
- Check logs for errors
- Ensure environment variables are set
- Verify NVIDIA_API_KEY is correct

### Slow Response
- Free tier spins down after 15 min
- First request wakes it up (~60s)
- Consider upgrading to Starter plan ($7/mo)

### Out of Memory
- Free tier: 512MB RAM
- Your app uses ~400-450MB
- If issues, upgrade to Starter (512MB guaranteed)

---

## 💡 Pro Tips

### Keep App Warm (Optional)
Use a service like [Uptime Robot](https://uptimerobot.com) to ping your app every 14 minutes (free tier allows):

```
https://guardianpdf.onrender.com/health
```

### Monitor Usage
Dashboard → Your Service → Metrics
- View bandwidth, CPU, memory
- Track response times

### Custom Domain (Optional)
1. Buy domain (e.g., Namecheap, GoDaddy)
2. Dashboard → Your Service → Settings → Custom Domains
3. Add CNAME record to your DNS
4. SSL auto-configured!

---

## 📝 Alternative: render.yaml

For infrastructure-as-code, use `render.yaml`:

```yaml
services:
  - type: web
    name: guardianpdf
    runtime: docker
    repo: https://github.com/aarushdubey/Guardian_PDF
    region: singapore
    plan: free
    envVars:
      - key: LLM_PROVIDER
        value: nvidia
      - key: NVIDIA_API_KEY
        sync: false
    disk:
      name: chroma-data
      mountPath: /data/chroma_db
      sizeGB: 1
```

Then: Dashboard → "New" → "Blueprint" → Connect repo

---

## 🎓 Next Steps After Deployment

1. ✅ Test all API endpoints via `/docs`
2. ✅ Upload a sample PDF
3. ✅ Run a query to verify RAG works
4. ✅ Test AI detection feature
5. ✅ Add live URL to your resume/portfolio
6. ✅ Share with potential employers!

---

## 💰 Cost Comparison

| Platform | Free Tier | Pro Plan |
|----------|-----------|----------|
| Render | ✅ 512MB, sleeps | $7/mo |
| Railway | ✅ $5 credit | $20/mo |
| Fly.io | ✅ $5 credit* | $2-5/mo |
| Heroku | ❌ Removed | $7/mo |

*Requires credit card

**Winner**: Render.com (no card, good free tier)

---

## 🚀 Ready to Deploy?

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your `Guardian_PDF` repo
4. Follow the steps above
5. Deploy!

**Need help?** Check the logs or let me know!
