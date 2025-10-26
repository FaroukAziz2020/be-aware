# 🛡️ BE AWARE

### Food Allergen & Nutrition Extractor

> **Stay safe with every bite.** Upload any food product PDF to instantly detect 10 allergens and extract 6 key nutritional values using OCR + AI.

<div align="center">

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-138.68.92.157-blue?style=for-the-badge)](http://138.68.92.157)
[![API](https://img.shields.io/badge/📡_API-Port_8000-green?style=for-the-badge)](http://138.68.92.157:8000)
[![Developer Dashboard](https://img.shields.io/badge/🔧_Developer-Dashboard-orange?style=for-the-badge)](http://138.68.92.157:8000/developer)

</div>

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📄 Smart PDF Processing
- **Drag & drop** or select any food label PDF
- **OCR for scanned PDFs** with Tesseract
- Support for **17+ languages**
- Handles both digital and image-based PDFs

</td>
<td width="50%">

### 🤖 AI-Powered Analysis
- **DeepSeek LLM** via OpenRouter
- Structured JSON extraction
- Intelligent text parsing
- High accuracy allergen detection

</td>
</tr>
<tr>
<td>

### 🔍 Comprehensive Detection
**10 EU-Regulated Allergens:**
- Gluten • Egg • Crustaceans • Fish
- Peanut • Soy • Milk • Tree Nuts
- Celery • Mustard

</td>
<td>

### 📊 Nutrition Facts
**6 Key Values Extracted:**
- Energy • Fat • Carbohydrate
- Sugar • Protein • Sodium

</td>
</tr>
<tr>
<td>

### 🌍 Multi-Language Support
- 🇬🇧 English
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇭🇺 Magyar

</td>
<td>

### 🎨 Modern UX
- 🌓 Dark/Light mode toggle
- 📱 Fully responsive design
- 📥 PDF report download
- ⚡ Real-time progress feedback

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

### Frontend
```
React 18 + Vite          →  Modern build tooling
i18next                  →  Internationalization
react-toastify           →  Toast notifications
Lucide Icons             →  Icon system
CSS Custom Properties    →  Dynamic theming
XMLHttpRequest           →  Upload progress tracking
```

### Backend
```
FastAPI                  →  High-performance web framework
PyPDF2                   →  Digital PDF text extraction
pdf2image + Pytesseract  →  OCR engine
OpenRouter + DeepSeek    →  LLM integration
ReportLab                →  PDF generation
Uvicorn                  →  ASGI server
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+**
- **Tesseract OCR**
  - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-hun`
- **Poppler** (PDF to image conversion)
  - Windows: [Download](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH
  - macOS: `brew install poppler`
  - Linux: `sudo apt install poppler-utils`

---

## 📦 Installation

### 1️⃣ Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Create `.env` file in `backend/`:**

```env
# Required: OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: OCR languages (defaults shown)
OCR_LANGUAGES=eng+deu+fra+spa+ita+por+hun+pol+ces+slk+ron+bul+hrv+slv+est+lav+lit

# Optional: Upload limits
MAX_UPLOAD_SIZE_BYTES=15728640  # 15MB

# Optional: CORS origins
CORS_ORIGINS=*
```

**Start the server:**

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

✅ **Backend running at:** `http://138.68.92.157:8000`

---

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

**Update `.env` in `frontend/`:**

```env
VITE_API_URL=http://138.68.92.157:8000
```

**Deploy to Nginx:**

```bash
sudo mkdir -p /var/www/be-aware
sudo cp -r dist/* /var/www/be-aware/
```

**Configure Nginx** (`/etc/nginx/sites-available/be-aware`):

```nginx
server {
    listen 80;
    server_name _;

    root /var/www/be-aware;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Enable and reload:**

```bash
sudo ln -s /etc/nginx/sites-available/be-aware /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

✅ **Frontend running at:** `http://138.68.92.157`

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check (all services) |
| `GET` | `/developer` | Interactive developer dashboard |
| `GET` | `/supported-languages` | List available OCR languages |
| `POST` | `/upload` | Analyze PDF (`multipart/form-data`) |
| `POST` | `/generate-pdf` | Generate report PDF (`application/json`) |

---

## 🧪 Testing

1. **Developer Dashboard:** [http://138.68.92.157:8000/developer](http://138.68.92.157:8000/developer)
2. **Frontend Upload:** [http://138.68.92.157](http://138.68.92.157)
3. **API Testing:** Use curl, Postman, or the built-in dashboard

**Example curl request:**

```bash
curl -X POST "http://138.68.92.157:8000/upload" \
  -F "file=@your-food-label.pdf"
```

---

## 👨‍💻 Author

**Farouk Aziz (BQ2AQM)**  
📧 farouk.aziz@mailbox.unideb.hu