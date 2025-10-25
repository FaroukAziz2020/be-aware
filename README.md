# BE AWARE – Food Allergen & Nutrition Extractor

**Stay safe with every bite.**  
Upload any food product **PDF** (text-based or scanned) to instantly detect **10 allergens** and extract **6 key nutritional values** using **OCR + AI**.

---

## 🌐 Live Demo

**Frontend:** [https://be-aware.vercel.app](https://be-aware.vercel.app)  
**Backend API:** [https://be-aware-backend.onrender.com](https://be-aware-backend.onrender.com)  
*(Replace with your actual deployed URLs after deployment)*

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
- **uvicorn** – ASGI server
- **python-dotenv** – Environment configuration

---

## 🚀 Setup & Running Locally

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Tesseract OCR** installed:
  - **Windows**: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu tesseract-ocr-fra`

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

# Optional: Tesseract path (Windows only, if not in default location)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Optional: OCR languages (defaults shown below)
OCR_LANGUAGES=eng+deu+fra+spa+ita+por+hun+pol+ces+slk+ron+bul+hrv+slv+est+lav+lit

# Optional: Upload limits
MAX_UPLOAD_SIZE_BYTES=15728640  # 15MB default
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
VITE_API_URL=http://127.0.0.1:8000/upload
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
uvicorn==0.24.0
python-dotenv==1.0.0
openai==1.3.5
pytesseract==0.3.10
pdf2image==1.16.3
PyPDF2==3.0.1
reportlab==4.0.7
python-multipart==0.0.6
```

**System Dependencies:**
- **Tesseract OCR** - For text extraction from images
- **Poppler** - For PDF to image conversion
  - **Windows**: [Download here](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH
  - **macOS**: `brew install poppler`
  - **Linux**: `sudo apt install poppler-utils`

---

## 🌍 Deployment Guide

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
   Value: https://your-backend.onrender.com/upload
   ```
   *(Add this after backend is deployed)*
6. Click **Deploy**

---

### Backend → Render (Free Tier)

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repository
3. **Configure:**
   ```
   Name: be-aware-backend
   Region: Frankfurt (or closest to you)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

4. **Add environment variables:**
   ```
   OPENROUTER_API_KEY=your_actual_key_here
   OCR_LANGUAGES=eng+deu+fra+hun
   ```

5. **Create `Aptfile` in `backend/` directory:**
   ```
   tesseract-ocr
   tesseract-ocr-eng
   tesseract-ocr-deu
   tesseract-ocr-fra
   tesseract-ocr-hun
   tesseract-ocr-spa
   tesseract-ocr-ita
   poppler-utils
   ```

6. Click **Create Web Service**
7. Wait 5-10 minutes for first deployment

**⚠️ Note:** Free tier has cold starts (~50 seconds). First request may be slow.

---

### Update Frontend with Backend URL

After backend is deployed on Render:

1. Copy your Render backend URL: `https://your-app.onrender.com`
2. Go to Vercel Dashboard → Your Project → **Settings** → **Environment Variables**
3. Edit `VITE_API_URL`:
   ```
   VITE_API_URL=https://your-app.onrender.com/upload
   ```
4. **Redeploy** (Vercel will auto-redeploy)

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
curl -X POST "http://127.0.0.1:8000/upload" \
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

## 🐛 Troubleshooting

### Backend Issues

**LLM Not Working?**
- ✅ Check `.env` has `OPENROUTER_API_KEY`
- ✅ Verify key at [openrouter.ai](https://openrouter.ai)
- ✅ Check `/developer` dashboard for status
- ✅ Look at terminal logs for errors

**OCR Not Working?**
- ✅ Install Tesseract OCR
- ✅ Windows: Set `TESSERACT_CMD` in `.env`
- ✅ Check `/developer` dashboard for Tesseract status
- ✅ Test: `tesseract --version` in terminal

**Poppler Error (pdf2image)?**
- ✅ Install Poppler (see dependencies section)
- ✅ Windows: Add Poppler `bin/` folder to PATH
- ✅ Restart terminal after installation

### Frontend Issues

**API Connection Failed?**
- ✅ Check backend is running on `http://127.0.0.1:8000`
- ✅ Verify `VITE_API_URL` in frontend `.env`
- ✅ Check CORS settings in `config.py`
- ✅ Open browser console (F12) for errors

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
Developer_Test/
│
├── backend/
│   ├── .env                      # Environment variables
│   ├── .gitignore               
│   ├── requirements.txt          # Python dependencies
│   ├── Aptfile                   # System packages for Render
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
│   │   ├── App.jsx               # Main app component
│   │   ├── App.css               # Global styles
│   │   ├── i18n.js               # Internationalization
│   │   └── components/           # React components
│   │       ├── FileUploader.jsx
│   │       ├── ProgressBar.jsx
│   │       ├── AllergensDisplay.jsx
│   │       ├── NutritionDisplay.jsx
│   │       ├── ResultsSection.jsx
│   │       ├── LanguageSelector.jsx
│   │       └── ThemeToggle.jsx
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
│
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```


## 👤 Author

**Farouk Aziz** (BQ2AQM)  
📧 farouk.aziz@mailbox.unideb.hu