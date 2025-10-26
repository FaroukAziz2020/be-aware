import os
import platform
import pathlib
from dotenv import load_dotenv

# Load environment variables
env_path = pathlib.Path(__file__).parent / ".env"
if not env_path.exists():
    env_path = None

load_dotenv(dotenv_path=env_path)


# Determine default Tesseract path based on operating system
if platform.system() == 'Windows':
    DEFAULT_TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    DEFAULT_TESSERACT_PATH = "tesseract"


class Config:
    """Application configuration"""

    # App Info
    APP_TITLE = "BE AWARE - Food Allergen Extractor API"
    APP_DESCRIPTION = "Extract allergens and nutrition from food product PDFs (multi-language, OCR + LLM)"
    APP_VERSION = "2.0.0"

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Upload limits
    MAX_UPLOAD_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", 15 * 1024 * 1024))

    # OCR Configuration
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", DEFAULT_TESSERACT_PATH)
    OCR_LANGUAGES = os.getenv(
        "OCR_LANGUAGES",
        "eng+deu+fra+spa+ita+por+hun+pol+ces+slk+ron+bul+hrv+slv+est+lav+lit"
    )

    # LLM Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL = "deepseek/deepseek-chat-v3.1"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 2000
    LLM_TIMEOUT = 30
    LLM_MAX_RETRIES = 3

    # Text extraction
    MAX_TEXT_CHARS = 6000  # For LLM prompt truncation
    MIN_TEXT_LENGTH = 100  # Minimum text before triggering OCR

    # PDF to Image conversion
    PDF_DPI = 300
    PDF_FORMAT = "png"

    # Tesseract OCR config
    TESSERACT_PSM = 3  # Page segmentation mode
    TESSERACT_OEM = 3  # OCR Engine mode