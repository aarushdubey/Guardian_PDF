# Setting Up NVIDIA AI API for GuardianPDF

## ✅ What Was Changed

GuardianPDF now supports **NVIDIA AI API** (in addition to Ollama)!

**Benefits**:
- ✅ No local Ollama required
- ✅ More powerful models (Llama 3 70B)
- ✅ Faster responses
- ✅ No GPU needed locally

---

## 🔑 Step 1: Add Your NVIDIA API Key

### Option A: Edit .env File (Recommended)

Open the `.env` file and replace `nvapi-YOUR_KEY_HERE` with your actual key:

```bash
cd /Users/aarushdubey/Downloads/guardian_pdf
nano .env  # or use any text editor
```

Change this line:
```
NVIDIA_API_KEY=nvapi-YOUR_KEY_HERE
```

To:
```
NVIDIA_API_KEY=nvapi-YOUR_ACTUAL_KEY
```

Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

### Option B: Set Environment Variable

```bash
export NVIDIA_API_KEY="nvapi-YOUR_ACTUAL_KEY"
```

---

## 🚀 Step 2: Start GuardianPDF

```bash
cd /Users/aarushdubey/Downloads/guardian_pdf
./start_server.sh
```

You should see:
```
🚀 Initializing GuardianPDF...
✅ NVIDIA AI ready: meta/llama3-70b-instruct
✅ GuardianPDF ready with security auditing!
   Provider: NVIDIA
   Model: meta/llama3-70b-instruct
```

---

## 🧪 Step 3: Test It

### Quick Test (No PDF needed)
```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "service": "GuardianPDF - Audit-First Edition",
  "status": "online"
}
```

### Full Test with PDF
```bash
# In another terminal
cd /Users/aarushdubey/Downloads/guardian_pdf
source venv/bin/activate

# Upload a PDF
python test_api.py path/to/your.pdf

# Or manually
curl -X POST http://localhost:8000/upload_pdf -F "file=@test.pdf"
```

---

## 🎯 Available NVIDIA Models

You can change the model in `.env`:

```bash
# Options (edit NVIDIA_MODEL in .env):
NVIDIA_MODEL=meta/llama3-70b-instruct    # Default, best quality
NVIDIA_MODEL=meta/llama3-8b-instruct     # Faster, smaller
NVIDIA_MODEL=mistralai/mixtral-8x7b-instruct-v0.1  # Alternative
```

---

## 🔄 Switching Between NVIDIA and Ollama

Edit `.env`:

```bash
# Use NVIDIA (recommended if you have API key)
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=nvapi-YOUR_KEY

# OR use Ollama (local, free, but requires setup)
LLM_PROVIDER=ollama
```

Then restart the server.

---

## ⚠️ Troubleshooting

### "NVIDIA_API_KEY not found"
- Check `.env` file exists in `/Users/aarushdubey/Downloads/guardian_pdf`
- Ensure no spaces around the `=` sign
- Make sure key starts with `nvapi-`

### "Error calling NVIDIA"
- Verify your API key is valid
- Check internet connection
- Try a different model

### "Falling back to Ollama"
- Means NVIDIA key wasn't found
- GuardianPDF will try to use Ollama instead
- Either fix the NVIDIA key or install Ollama

---

## 📊 What Changed in the Code

1. **Updated `rag_pipeline.py`**: Now supports both NVIDIA and Ollama
2. **Updated `app.py`**: Reads configuration from environment variables
3. **Added `.env`**: Configuration file for API keys
4. **Added dependencies**: `openai` and `python-dotenv`

All changes are backward compatible - Ollama still works if no NVIDIA key is provided!

---

## ✅ Verification Checklist

- [ ] `.env` file exists with your NVIDIA API key
- [ ] Dependencies installed (`openai`, `python-dotenv`)
- [ ] Server starts without errors
- [ ] API responds to health check
- [ ] PDF upload works
- [ ] Queries return answers (powered by NVIDIA!)

---

**You're all set! GuardianPDF is now powered by NVIDIA AI 🚀**

