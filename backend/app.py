import time
import logging
from typing import Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse

from config import Config
from llm import LLMClient
from TextExtraction import OCRService
from pdf_analyzer import PDFAnalyzer
from pdf_generator import PDFGenerator

# -------------------------
# Logging configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("be_aware_backend")

# -------------------------
# Initialize Services
# -------------------------
llm_client = LLMClient()
pdf_analyzer = PDFAnalyzer(llm_client)
pdf_generator = PDFGenerator()

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    version=Config.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Root & Info Endpoints
# -------------------------
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "✅ BE AWARE - Multi-Language Food Info Extractor",
        "version": Config.APP_VERSION,
        "endpoints": {
            "health": "/health - Health check",
            "developer": "/developer - Developer dashboard (HTML)",
            "upload": "/upload (POST) - Upload and analyze PDF",
            "generate_pdf": "/generate-pdf (POST) - Generate report PDF",
            "supported_languages": "/supported-languages - OCR language info"
        },
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    ocr_status = OCRService.test_ocr()

    return {
        "status": "healthy" if llm_client.configured else "degraded",
        "timestamp": time.time(),
        "services": {
            "llm": {
                "configured": llm_client.configured,
                "model": Config.LLM_MODEL if llm_client.configured else None
            },
            "ocr": {
                "available": ocr_status["success"],
                "languages_count": len(ocr_status.get("available_languages", [])) if ocr_status["success"] else 0
            }
        }
    }


@app.get("/supported-languages")
def supported_languages():
    """Get OCR supported languages"""
    result = OCRService.test_ocr()
    return {
        "success": result["success"],
        "tesseract_installed_languages": result.get("available_languages", []),
        "configured_string": Config.OCR_LANGUAGES,
        "tesseract_path": result.get("tesseract_path")
    }


# -------------------------
# Developer Dashboard
# -------------------------
@app.get("/developer", response_class=HTMLResponse)
async def developer_dashboard():
    """Interactive developer dashboard to test all services"""

    # Test all services
    llm_test = llm_client.test_connection()
    ocr_test = OCRService.test_ocr()

    # Build status HTML
    def status_badge(success: bool) -> str:
        if success:
            return '<span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 6px; font-weight: 600;">✓ Working</span>'
        return '<span style="background: #ef4444; color: white; padding: 4px 12px; border-radius: 6px; font-weight: 600;">✗ Failed</span>'

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BE AWARE - Developer Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5rem;
            }}
            .subtitle {{
                color: #666;
                margin-bottom: 40px;
                font-size: 1.1rem;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                background: #f9fafb;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
            }}
            .section h2 {{
                color: #333;
                margin-bottom: 15px;
                font-size: 1.5rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .status-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                background: white;
                border-radius: 8px;
                margin-bottom: 10px;
            }}
            .status-label {{
                font-weight: 600;
                color: #555;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}
            .info-card {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }}
            .info-card strong {{
                color: #667eea;
                display: block;
                margin-bottom: 5px;
            }}
            .info-card p {{
                color: #666;
                font-size: 0.9rem;
            }}
            .code-block {{
                background: #1e293b;
                color: #e2e8f0;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                overflow-x: auto;
                margin-top: 10px;
            }}
            .warning {{
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}
            .warning strong {{
                color: #92400e;
            }}
            .success {{
                background: #d1fae5;
                border-left: 4px solid #10b981;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}
            .success strong {{
                color: #065f46;
            }}
            .endpoints {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
            }}
            .endpoint {{
                padding: 10px;
                border-bottom: 1px solid #e5e7eb;
            }}
            .endpoint:last-child {{
                border-bottom: none;
            }}
            .endpoint code {{
                background: #f3f4f6;
                padding: 2px 8px;
                border-radius: 4px;
                color: #667eea;
                font-weight: 600;
            }}
            .btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                text-decoration: none;
                display: inline-block;
                margin-top: 10px;
            }}
            .btn:hover {{
                background: #5568d3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛠️ BE AWARE Developer Dashboard</h1>
            <p class="subtitle">System Status & Service Testing</p>

            <!-- Overall Status -->
            <div class="section">
                <h2>📊 Overall System Status</h2>
                <div class="status-row">
                    <span class="status-label">Backend API</span>
                    {status_badge(True)}
                </div>
                <div class="status-row">
                    <span class="status-label">LLM Service (OpenRouter/DeepSeek)</span>
                    {status_badge(llm_test["success"])}
                </div>
                <div class="status-row">
                    <span class="status-label">OCR Service (Tesseract)</span>
                    {status_badge(ocr_test["success"])}
                </div>
            </div>

            <!-- LLM Details -->
            <div class="section">
                <h2>🤖 LLM Configuration</h2>
                {'<div class="success"><strong>✓ LLM is configured and working</strong></div>' if llm_test["success"] else '<div class="warning"><strong>⚠ LLM is not configured</strong><br>Set OPENROUTER_API_KEY in your .env file</div>'}

                <div class="info-grid">
                    <div class="info-card">
                        <strong>Model</strong>
                        <p>{Config.LLM_MODEL}</p>
                    </div>
                    <div class="info-card">
                        <strong>Temperature</strong>
                        <p>{Config.LLM_TEMPERATURE}</p>
                    </div>
                    <div class="info-card">
                        <strong>Max Tokens</strong>
                        <p>{Config.LLM_MAX_TOKENS}</p>
                    </div>
                    <div class="info-card">
                        <strong>Timeout</strong>
                        <p>{Config.LLM_TIMEOUT}s</p>
                    </div>
                </div>

                {f'<div class="code-block">Test Response: {llm_test.get("response", "N/A")}</div>' if llm_test["success"] else ''}
            </div>

            <!-- OCR Details -->
            <div class="section">
                <h2>📷 OCR Configuration</h2>
                {'<div class="success"><strong>✓ Tesseract is installed and working</strong></div>' if ocr_test["success"] else '<div class="warning"><strong>⚠ Tesseract is not configured</strong><br>Install Tesseract OCR and set TESSERACT_CMD in .env</div>'}

                <div class="info-grid">
                    <div class="info-card">
                        <strong>Tesseract Path</strong>
                        <p style="word-break: break-all;">{ocr_test.get("tesseract_path", "Not set")}</p>
                    </div>
                    <div class="info-card">
                        <strong>Languages Available</strong>
                        <p>{len(ocr_test.get("available_languages", []))} languages</p>
                    </div>
                </div>

                {f'<div class="code-block">Available Languages: {", ".join(ocr_test.get("available_languages", [])[:20])}...</div>' if ocr_test["success"] else ''}

                <div class="info-card" style="margin-top: 15px;">
                    <strong>Configured OCR Languages</strong>
                    <p>{Config.OCR_LANGUAGES}</p>
                </div>
            </div>

            <!-- API Configuration -->
            <div class="section">
                <h2>⚙️ API Configuration</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <strong>App Version</strong>
                        <p>{Config.APP_VERSION}</p>
                    </div>
                    <div class="info-card">
                        <strong>Max Upload Size</strong>
                        <p>{Config.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024):.1f} MB</p>
                    </div>
                    <div class="info-card">
                        <strong>CORS Origins</strong>
                        <p>{", ".join(Config.CORS_ORIGINS)}</p>
                    </div>
                    <div class="info-card">
                        <strong>LLM Retries</strong>
                        <p>{Config.LLM_MAX_RETRIES}</p>
                    </div>
                </div>
            </div>

            <!-- API Endpoints -->
            <div class="section">
                <h2>🔗 Available Endpoints</h2>
                <div class="endpoints">
                    <div class="endpoint">
                        <code>GET /</code> - API information
                    </div>
                    <div class="endpoint">
                        <code>GET /health</code> - Health check
                    </div>
                    <div class="endpoint">
                        <code>GET /developer</code> - This dashboard
                    </div>
                    <div class="endpoint">
                        <code>GET /supported-languages</code> - OCR languages
                    </div>
                    <div class="endpoint">
                        <code>POST /upload</code> - Upload and analyze PDF
                    </div>
                    <div class="endpoint">
                        <code>POST /generate-pdf</code> - Generate report PDF
                    </div>
                </div>

                <a href="/docs" class="btn">📚 View API Documentation</a>
            </div>

            <!-- Quick Test Section -->
            <div class="section">
                <h2>🧪 Quick Tests</h2>
                <div class="info-card">
                    <strong>Test Health Check</strong>
                    <p>Check all services status</p>
                    <a href="/health" class="btn" target="_blank">Run Health Check</a>
                </div>

                <div class="info-card" style="margin-top: 15px;">
                    <strong>Test OCR Languages</strong>
                    <p>View all supported OCR languages</p>
                    <a href="/supported-languages" class="btn" target="_blank">View Languages</a>
                </div>
            </div>

            <!-- Troubleshooting -->
            <div class="section">
                <h2>🔧 Troubleshooting</h2>

                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">LLM Not Working?</strong>
                    <ol style="margin-left: 20px; margin-top: 10px; color: #666;">
                        <li>Create a <code>.env</code> file in the backend directory</li>
                        <li>Add: <code>OPENROUTER_API_KEY=your_key_here</code></li>
                        <li>Get API key from <a href="https://openrouter.ai" target="_blank" style="color: #667eea;">openrouter.ai</a></li>
                        <li>Restart the server</li>
                    </ol>
                </div>

                <div>
                    <strong style="color: #333;">OCR Not Working?</strong>
                    <ol style="margin-left: 20px; margin-top: 10px; color: #666;">
                        <li>Install Tesseract OCR from <a href="https://github.com/tesseract-ocr/tesseract" target="_blank" style="color: #667eea;">GitHub</a></li>
                        <li>Windows: Install to default path or set <code>TESSERACT_CMD</code> in .env</li>
                        <li>Linux/Mac: <code>sudo apt install tesseract-ocr</code> or <code>brew install tesseract</code></li>
                        <li>Restart the server</li>
                    </ol>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


# -------------------------
# Main Endpoints
# -------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), language: str = Form("en")):
    """
    Upload and analyze a PDF file

    Form fields:
    - file: PDF file
    - language: language code (en, fr, de, hu)
    """
    # Validate file
    filename = getattr(file, "filename", "uploaded.pdf")
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are supported.")

    # Read file
    try:
        contents = await file.read()
    except Exception as e:
        logger.exception("Failed to read uploaded file: %s", e)
        raise HTTPException(status_code=400, detail="Failed to read uploaded file.")

    # Check size
    if len(contents) > Config.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size is {Config.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024):.1f} MB."
        )

    # Analyze
    start = time.time()
    result = pdf_analyzer.analyze(contents, filename=filename, language=language)
    duration = round(time.time() - start, 2)

    # Response
    response_payload = {
        "success": "error" not in result,
        "filename": filename,
        "file_size_bytes": len(contents),
        "processing_time_seconds": duration,
        "data": result
    }

    return JSONResponse(content=response_payload)


@app.post("/generate-pdf")
async def generate_pdf(payload: Dict[str, Any]):
    """
    Generate a PDF report from analysis data

    Body: JSON with allergens, nutritional_values, and language
    """
    try:
        pdf_bytes = pdf_generator.generate(payload)

        headers = {
            "Content-Disposition": 'attachment; filename="be_aware_report.pdf"'
        }

        return StreamingResponse(
            pdf_bytes,
            media_type="application/pdf",
            headers=headers
        )

    except Exception as e:
        logger.exception("❌ PDF generation failed: %s", e)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting BE AWARE backend on http://127.0.0.1:8000")
    logger.info("📊 Developer dashboard: http://127.0.0.1:8000/developer")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)