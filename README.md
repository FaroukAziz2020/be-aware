# BE AWARE – Food Allergen & Nutrition Extractor

**Stay safe with every bite.**  
Upload any food product **PDF** (text-based or scanned) to instantly detect **10 allergens** and extract **6 key nutritional values** using **OCR + AI**.

---

## 🌐 Live Demo

**Frontend:** [https://be-aware-nutrition-qz7dgxgt1-farouk-azizs-projects.vercel.app](https://be-aware-nutrition-qz7dgxgt1-farouk-azizs-projects.vercel.app)  
**Backend API:** [https://be-aware-backend.onrender.com](https://be-aware-backend.onrender.com)  
**Developer Dashboard:** [https://be-aware-backend.onrender.com/developer](https://be-aware-backend.onrender.com/developer)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **PDF Upload** | Drag & drop or select any food label PDF |
| **OCR for Scanned PDFs** | Uses **Tesseract OCR** (multi-language support: 17+ languages) |
| **AI-Powered Extraction** | **DeepSeek LLM** via OpenRouter parses unstructured text |
| **Allergen Detection** | 10 EU-regulated allergens: `Gluten`, `Egg`, `Crustaceans`, `Fish`, `Peanut`, `Soy`, `Milk`, `Tree Nuts`, `Celery`, `Mustard` |
| **Nutrition Facts** | 6 key values: `Energy`, `Fat`, `Carbohydrate`, `Sugar`, `Protein`, `Sodium` |
| **Multi-Language UI** | **English · Français · Deutsch · Magyar** |
| **Dark Mode** | Toggle between light/dark themes with persistent preference |
| **PDF Report Download** | Generate & download a formatted **awareness report** in selected language |
| **Responsive Design** | Mobile, tablet, desktop ready |
| **Progress Feedback** | Real-time upload + analysis progress bar |
| **Error Handling** | User-friendly toasts for all states |
| **Developer Dashboard** | Built-in `/developer` endpoint to test all services |
| **Docker Deployment** | Containerized backend for reliable OCR deployment |

---

## 🛠️ Tech Stack

### Frontend
- **React 18** + **Vite**
- **i18next** – Internationalization (4 languages)
- **react-toastify** – Toast notifications
- **Lucide Icons** – Modern icon system
- **CSS Custom Properties** – Dynamic theming system
- **XMLHttpRequest + Progress Events** – Upload tracking with real-time feedback

### Backend
- **FastAPI** – Modern Python web framework
- **PyPDF2** – Extract text from digital PDFs
- **pdf2image + Pytesseract** – OCR for image-based/scanned PDFs
- **OpenRouter + DeepSeek** – LLM for structured JSON extraction
- **ReportLab** – Generate downloadable PDF reports with localization
- **Docker** – Containerized deployment with system dependencies
- **uvicorn** – ASGI server
- **python-dotenv** – Environment configuration

---

## 🚀 Setup & Running Locally

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Tesseract OCR** installed:
  - **Windows**: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-hun`
- **Poppler** (for PDF to image conversion):
  - **Windows**: [Download here](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH
  - **macOS**: `brew install poppler`
  - **Linux**: `sudo apt install poppler-utils`

---

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Create `.env` file in `backend/`:**

```env
# Required: OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: OCR languages (defaults shown below)
OCR_LANGUAGES=eng+deu+fra+spa+ita+por+hun+pol+ces+slk+ron+bul+hrv+slv+est+lav+lit

# Optional: Upload limits
MAX_UPLOAD_SIZE_BYTES=15728640  # 15MB default

# Optional: CORS origins (for production)
CORS_ORIGINS=*
```

**Get your OpenRouter API key:**
1. Visit [https://openrouter.ai](https://openrouter.ai)
2. Sign up/login
3. Go to **Keys** section
4. Create new key
5. Copy to `.env` file

**Start server:**

```bash
python app.py
# or
uvicorn app:app --reload --port 8000
```

**Backend URLs:**
- API: `http://127.0.0.1:8000`
- Documentation: `http://127.0.0.1:8000/docs`
- Developer Dashboard: `http://127.0.0.1:8000/developer` ⭐

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

**Create `.env` in `frontend/`:**

```env
VITE_API_URL=http://127.0.0.1:8000
```

**Start dev server:**

```bash
npm run dev
```

**Frontend URL:** `http://localhost:5173`

---

## 🧪 Testing the Application

### 1. Test Backend Services
Visit the developer dashboard: `http://127.0.0.1:8000/developer`

This interactive dashboard shows:
- ✅ LLM service status
- ✅ OCR/Tesseract status
- ✅ Available OCR languages
- ✅ Configuration details
- ✅ Quick test buttons

### 2. Test API Endpoints
Visit the auto-generated API documentation: `http://127.0.0.1:8000/docs`

Try these endpoints:
- `GET /health` - Check all services
- `GET /supported-languages` - View OCR languages
- `POST /upload` - Upload a PDF for analysis
- `POST /generate-pdf` - Generate a report

### 3. Test Frontend
1. Open `http://localhost:5173`
2. Try uploading a food label PDF
3. Test language switching (EN/FR/DE/HU)
4. Toggle dark mode
5. Download PDF report

---

## 📦 Backend Dependencies

**Python Packages** (`requirements.txt`):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
openai==1.3.5
httpx==0.24.1
httpcore==0.17.3
pytesseract==0.3.10
pdf2image==1.16.3
PyPDF2==3.0.1
reportlab==4.0.7
python-multipart==0.0.6
```

**System Dependencies:**
- **Tesseract OCR** - For text extraction from images
- **Poppler** - For PDF to image conversion

---

## 🌐 Deployment Guide

### Frontend → Vercel (Free)

1. **Push code to GitHub**
2. Go to [vercel.com](https://vercel.com) → **Import Project**
3. Select your repository
4. **Configure:**
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. **Add environment variable:**
   ```
   Name: VITE_API_URL
   Value: https://be-aware-backend.onrender.com
   ```
   ⚠️ **Important:** No trailing slash, no `/upload` path
6. Click **Deploy**

---

### Backend → Render with Docker (Free Tier)

#### Step 1: Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.13-slim

# Install system dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    tesseract-ocr-fra \
    tesseract-ocr-hun \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 10000

# Start command
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}
```

#### Step 2: Create .dockerignore

Create `backend/.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.env
venv/
.venv/
```

#### Step 3: Deploy to Render

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repository
3. **Configure:**
   ```
   Name: be-aware-backend
   Region: Frankfurt (or closest to you)
   Branch: main
   Root Directory: backend
   Environment: Docker
   Instance Type: Free
   ```

4. **Add environment variables in Render dashboard:**
   ```
   OPENROUTER_API_KEY=your_actual_key_here
   OCR_LANGUAGES=eng+deu+fra+hun
   CORS_ORIGINS=*
   ```

5. Click **Create Web Service**
6. Wait 5-10 minutes for first deployment

**✅ Why Docker?**
- Guarantees Tesseract OCR installation
- Consistent environment across local and production
- No Aptfile needed (system packages installed in Dockerfile)
- More reliable than native builds

**⚠️ Note:** Free tier has cold starts (~50 seconds). First request may be slow.

---

### Update Frontend with Backend URL

After backend is deployed on Render:

1. Copy your Render backend URL: `https://be-aware-backend.onrender.com`
2. Go to Vercel Dashboard → Your Project → **Settings** → **Environment Variables**
3. Update `VITE_API_URL`:
   ```
   VITE_API_URL=https://be-aware-backend.onrender.com
   ```
   ⚠️ **No `/upload` suffix needed** - the frontend adds endpoints automatically
4. **Redeploy** frontend (Vercel → Deployments → Redeploy)

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check (all services) |
| `GET` | `/developer` | Interactive developer dashboard |
| `GET` | `/supported-languages` | List OCR languages |
| `POST` | `/upload` | Analyze PDF (multipart/form-data) |
| `POST` | `/generate-pdf` | Generate report PDF (application/json) |

### Example: Upload PDF

```bash
curl -X POST "https://be-aware-backend.onrender.com/upload" \
  -F "file=@product_label.pdf" \
  -F "language=en"
```

**Response:**
```json
{
  "success": true,
  "filename": "product_label.pdf",
  "file_size_bytes": 245680,
  "processing_time_seconds": 3.42,
  "data": {
    "allergens": {
      "gluten": true,
      "milk": true,
      "egg": false,
      "soy": true,
      "peanut": false,
      "crustaceans": false,
      "fish": false,
      "tree_nuts": false,
      "celery": false,
      "mustard": false
    },
    "nutritional_values": {
      "energy": "2000 kJ / 478 kcal",
      "fat": "25g",
      "carbohydrate": "50g",
      "sugar": "8g",
      "protein": "7g",
      "sodium": "1.2g"
    },
    "metadata": {
      "ocr_used": false,
      "language_selected": "en",
      "confidence": "high"
    }
  }
}
```

---

## 🛠 Troubleshooting

### Backend Issues

**LLM Not Working?**
- ✅ Check environment variables in Render dashboard
- ✅ Verify `OPENROUTER_API_KEY` is set correctly
- ✅ Check `/developer` dashboard for status
- ✅ Look at Render logs for errors

**OCR Not Working on Render?**
- ✅ Ensure you're using Docker deployment (not native)
- ✅ Dockerfile includes all Tesseract packages
- ✅ Check Render logs for Tesseract installation
- ✅ Visit `/developer` to verify OCR status

**Local OCR Not Working?**
- ✅ Install Tesseract OCR for your OS
- ✅ Windows: Tesseract auto-detected at default path
- ✅ macOS/Linux: Tesseract should be in PATH
- ✅ Test: `tesseract --version` in terminal

**Poppler Error (pdf2image)?**
- ✅ Install Poppler for your OS
- ✅ Windows: Add Poppler `bin/` folder to PATH
- ✅ Restart terminal after installation

**httpx Compatibility Error?**
- ✅ Use pinned versions: `httpx==0.24.1`, `httpcore==0.17.3`
- ✅ These are compatible with `openai==1.3.5`

### Frontend Issues

**API Connection Failed?**
- ✅ Check backend is running
- ✅ Verify `VITE_API_URL` in Vercel environment variables
- ✅ Ensure no trailing slash in API URL
- ✅ Check CORS settings in `config.py`
- ✅ Open browser console (F12) for errors

**405 Method Not Allowed?**
- ✅ Verify `VITE_API_URL` points to correct backend
- ✅ URL should be base domain only (no `/upload`)
- ✅ Redeploy frontend after changing env vars

**Dark Mode Not Persisting?**
- ✅ Check browser allows localStorage
- ✅ Clear browser cache and reload
- ✅ Try in incognito/private mode

**Build Errors?**
- ✅ Delete `node_modules/` and `package-lock.json`
- ✅ Run `npm install` again
- ✅ Check Node.js version: `node --version` (should be 18+)

---

## 🎯 Project Structure

```
be-aware/
│
├── backend/
│   ├── .env                      # Environment variables
│   ├── .gitignore               
│   ├── .dockerignore             # Docker ignore file
│   ├── Dockerfile                # Docker configuration
│   ├── requirements.txt          # Python dependencies
│   ├── app.py                    # FastAPI application
│   ├── config.py                 # Configuration management
│   ├── llm.py                    # LLM client
│   ├── pdf_analyzer.py           # PDF analysis logic
│   ├── TextExtraction.py         # OCR service
│   └── pdf_generator.py          # Report generation
│
├── frontend/
│   ├── .env                      # API URL
│   ├── src/
│   │   ├── main.jsx              # React entry point
│   │   ├── app.jsx               # Main app component
│   │   ├── app.css               # Global styles
│   │   ├── i18n.js               # Internationalization
│   │   └── components/           # React components
│   │       ├── FileUploader.jsx
│   │       ├── ProgressBar.jsx
│   │       ├── AllergensDisplay.jsx
│   │       ├── NutritionDisplay.jsx
│   │       ├── ResultSection.jsx
│   │       ├── LanguageSelector.jsx
│   │       └── ThemeToggle.jsx
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
│
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

---

## 🔧 Key Configuration Files

### backend/config.py
- Auto-detects OS for Tesseract path (Windows vs Linux)
- Configures LLM settings (model, temperature, tokens)
- Sets OCR languages and upload limits
- Manages CORS origins

### backend/Dockerfile
- Uses Python 3.13-slim base image
- Installs Tesseract + language packs
- Installs Poppler for PDF conversion
- Sets up application environment

### frontend/.env
- `VITE_API_URL` - Backend base URL (no trailing slash)

---

## 💡 Tips & Best Practices

### Development
- Use the `/developer` dashboard to verify all services before testing uploads
- Check backend logs for detailed error messages
- Test with both text-based and scanned PDFs
- Try different languages to verify OCR support

### Deployment
- **Always use Docker for backend** - guarantees OCR reliability
- Pin all package versions to avoid breaking changes
- Set environment variables before deploying
- Monitor Render logs during first deployment
- Test `/health` endpoint after deployment

### Performance
- Free tier has cold starts - first request takes ~50s
- Subsequent requests are fast (~3-5s)
- Consider paid tier for production use
- Optimize PDF size before upload (max 15MB)

---

## 👤 Author

**Farouk Aziz** (BQ2AQM)  
📧 farouk.aziz@mailbox.unideb.hu