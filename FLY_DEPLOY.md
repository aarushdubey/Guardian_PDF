# GuardianPDF - Fly.io Deployment Guide

## ✅ Prerequisites
- [x] Fly.io CLI installed (`flyctl`)
- [x] Dockerfile configured
- [x] fly.toml configured

## 🚀 Deployment Steps

### Step 1: Authenticate with Fly.io
```bash
flyctl auth login
```
This will open your browser for authentication.

### Step 2: Create Fly.io App
```bash
flyctl apps create guardianpdf
```

### Step 3: Create Persistent Volume for ChromaDB
```bash
flyctl volumes create chroma_data --region bom --size 1
```

### Step 4: Set Environment Variables
```bash
flyctl secrets set NVIDIA_API_KEY="your-nvidia-api-key-here"
flyctl secrets set LLM_PROVIDER="nvidia"
flyctl secrets set NVIDIA_MODEL="meta/llama3-70b-instruct"
```

### Step 5: Deploy
```bash
flyctl deploy
```

This will:
- Build your Docker image
- Push to Fly.io registry
- Deploy to Mumbai region (bom)
- Set up persistent volume for vector store

### Step 6: Get Your Live URL
```bash
flyctl status
flyctl open
```

Your app will be live at: `https://guardianpdf.fly.dev`

## 📊 Monitoring

Check logs:
```bash
flyctl logs
```

Check app status:
```bash
flyctl status
```

SSH into machine:
```bash
flyctl ssh console
```

## 🔧 Configuration

### Scaling (if needed)
```bash
# Increase memory
flyctl scale memory 2048

# Add more instances
flyctl scale count 2
```

### Update Environment Variables
```bash
flyctl secrets set KEY=value
```

## 💰 Cost Estimate
- **Free tier**: 3 shared-cpu VMs with 256MB RAM
- **Current config**: 1GB RAM, 1 CPU = ~$5-7/month
- **Volume storage**: 1GB = Free (included)

## 🛠️ Troubleshooting

### Build fails
```bash
# Check build logs
flyctl logs --app guardianpdf

# Force rebuild
flyctl deploy --no-cache
```

### App not responding
```bash
# Restart app
flyctl apps restart guardianpdf

# Check health
flyctl checks list
```

## 🔐 Security Notes
- HTTPS enabled by default
- Environment variables encrypted
- Private networking available
- Volume data persisted

## 📝 Next Steps After Deployment
1. Test API endpoints: `https://guardianpdf.fly.dev/health`
2. Upload a PDF: `https://guardianpdf.fly.dev/docs`
3. Query your documents
4. Add custom domain (optional)
