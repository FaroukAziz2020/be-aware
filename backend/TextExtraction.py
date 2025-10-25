# TextExtraction.py - OCR Service and Testing
import logging
import pytesseract

from config import Config

logger = logging.getLogger("be_aware_backend")

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD


class OCRService:
    """OCR service for testing and configuration"""

    @staticmethod
    def test_ocr() -> dict:
        """
        Test OCR/Tesseract installation and get available languages.

        Returns:
            Dictionary with success status, available languages, and tesseract path
        """
        try:
            # Get available languages
            langs = pytesseract.get_languages()

            # Get tesseract version and path
            version = pytesseract.get_tesseract_version()

            logger.info("✅ Tesseract OCR test successful - version %s", version)
            logger.info("📋 Available languages: %s", ", ".join(langs))

            return {
                "success": True,
                "available_languages": langs,
                "tesseract_path": Config.TESSERACT_CMD,
                "version": str(version)
            }

        except Exception as e:
            logger.exception("❌ Tesseract OCR test failed: %s", e)
            return {
                "success": False,
                "error": str(e),
                "tesseract_path": Config.TESSERACT_CMD,
                "available_languages": []
            }

    @staticmethod
    def get_supported_languages() -> list:
        """
        Get list of supported OCR languages.

        Returns:
            List of language codes
        """
        try:
            return pytesseract.get_languages()
        except Exception as e:
            logger.exception("Failed to get tesseract languages: %s", e)
            return []