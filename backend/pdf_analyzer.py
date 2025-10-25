# pdf_analyzer.py - PDF Analysis and Text Extraction
import io
import json
import logging
from typing import Tuple, Dict, Any

from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
import pytesseract

from config import Config

logger = logging.getLogger("be_aware_backend")

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD


class PDFAnalyzer:
    """Handles PDF text extraction and LLM-based data extraction"""

    def __init__(self, llm_client):
        """
        Initialize PDFAnalyzer with an LLM client

        Args:
            llm_client: Instance of LLMClient for text analysis
        """
        self.llm_client = llm_client
        logger.info("✅ PDFAnalyzer initialized")

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> Tuple[str, bool]:
        """
        Try direct text extraction via PyPDF2; if insufficient, fallback to OCR.

        Args:
            pdf_bytes: PDF file contents as bytes

        Returns:
            Tuple of (extracted_text, ocr_used)
        """
        text = ""
        ocr_used = False

        try:
            logger.info("📄 Trying PyPDF2 text extraction")
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text() or ""
                except Exception:
                    page_text = ""
                if page_text.strip():
                    text += f"\n--- Page {i + 1} ---\n{page_text}"
            if text.strip():
                logger.info("✅ PyPDF2 extracted %d characters", len(text))
        except Exception as e:
            logger.warning("⚠️ PyPDF2 extraction error: %s", e)

        # If not enough text, use OCR
        if not text.strip() or len(text.strip()) < Config.MIN_TEXT_LENGTH:
            ocr_used = True
            logger.info("📷 Falling back to OCR (languages=%s)", Config.OCR_LANGUAGES)
            try:
                images = convert_from_bytes(
                    pdf_bytes,
                    dpi=Config.PDF_DPI,
                    fmt=Config.PDF_FORMAT
                )
                logger.info("🖼️ Converted PDF to %d images for OCR", len(images))

                for idx, img in enumerate(images):
                    logger.info("📸 OCR page %d/%d", idx + 1, len(images))
                    page_text = pytesseract.image_to_string(
                        img,
                        lang=Config.OCR_LANGUAGES,
                        config=f"--psm {Config.TESSERACT_PSM} --oem {Config.TESSERACT_OEM}"
                    )
                    if page_text and page_text.strip():
                        text += f"\n--- Page {idx + 1} (OCR) ---\n{page_text}"

                logger.info("✅ OCR extraction finished (total chars=%d)", len(text))
            except Exception as e:
                logger.exception("❌ OCR failed: %s", e)
                raise RuntimeError(f"OCR processing failed: {e}")

        if not text.strip():
            raise RuntimeError("No text could be extracted from the PDF (PyPDF2 and OCR both failed).")

        return text.strip(), ocr_used

    def extract_data_from_text(self, text: str) -> Dict[str, Any]:
        """
        Use LLM to extract structured allergen and nutrition data from text.

        Args:
            text: Extracted text from PDF

        Returns:
            Dictionary with allergens, nutritional_values, and metadata
        """
        # Truncate text if too long
        max_chars = Config.MAX_TEXT_CHARS
        if len(text) > max_chars:
            mid = max_chars // 2
            text = text[:mid] + "\n\n[... middle content truncated ...]\n\n" + text[-mid:]

        prompt = f"""
You are a multilingual food label analyzer. Extract allergen and nutritional data from this text.
Return JSON like:
{{
  "allergens": {{
    "gluten": true/false,
    "egg": true/false,
    "crustaceans": true/false,
    "fish": true/false,
    "peanut": true/false,
    "soy": true/false,
    "milk": true/false,
    "tree_nuts": true/false,
    "celery": true/false,
    "mustard": true/false
  }},
  "nutritional_values": {{
    "energy": "...",
    "fat": "...",
    "carbohydrate": "...",
    "sugar": "...",
    "protein": "...",
    "sodium": "..."
  }}
}}

Text:
{text}"""

        try:
            raw = self.llm_client.call(prompt)
        except Exception as e:
            logger.exception("❌ LLM call failed: %s", e)
            return self._empty_result(error="LLM extraction failed")

        # Parse LLM response
        return self._parse_llm_response(raw)

    def _parse_llm_response(self, raw: str) -> Dict[str, Any]:
        """Parse and validate LLM JSON response"""
        try:
            clean = raw.strip()

            # Remove code block markers if present
            if clean.startswith("```"):
                parts = clean.split("\n")
                if len(parts) > 2:
                    clean = "\n".join(parts[1:-1])

            # Extract JSON from response
            start = clean.find("{")
            end = clean.rfind("}")
            if start != -1 and end != -1:
                clean = clean[start:end + 1]

            data = json.loads(clean)

            # Ensure required fields
            if "allergens" not in data:
                data["allergens"] = {}
            if "nutritional_values" not in data:
                data["nutritional_values"] = {}
            if "metadata" not in data:
                data["metadata"] = {"per_100g": True, "language_detected": "unknown", "confidence": "medium"}

            # Normalize allergens
            for allergen in ["gluten", "egg", "crustaceans", "fish", "peanut", "soy",
                             "milk", "tree_nuts", "celery", "mustard"]:
                if allergen not in data["allergens"]:
                    data["allergens"][allergen] = False

            # Normalize nutrition values
            for nutrient in ["energy", "fat", "carbohydrate", "sugar", "protein", "sodium"]:
                if nutrient not in data["nutritional_values"]:
                    data["nutritional_values"][nutrient] = "Not available"
                else:
                    # Clean up nutrition values
                    val = data["nutritional_values"][nutrient]
                    if isinstance(val, str):
                        val = self._normalize_nutrition_value(val)
                        data["nutritional_values"][nutrient] = val

            logger.info("✅ Parsed LLM JSON successfully")
            return data

        except json.JSONDecodeError as e:
            logger.exception("❌ JSON decode failed: %s", e)
            return self._empty_result(error="Failed to parse LLM response as JSON", raw_response=raw[:1000])
        except Exception as e:
            logger.exception("❌ Unexpected error parsing LLM output: %s", e)
            return self._empty_result(error="Data extraction error", raw_response=raw[:1000])

    def _normalize_nutrition_value(self, val: str) -> str:
        """Normalize nutrition value strings"""
        import re

        val = val.strip()

        # Remove "(as salt)" or similar parenthetical notes
        val = re.sub(
            r'\s*\((as\s+)?salt\)|\((comme\s+)?sel\)|\((als\s+)?Salz\)|\(sóként\)',
            '', val, flags=re.IGNORECASE
        )
        val = val.strip()

        # Check for "not available" phrases in multiple languages
        val_lower = val.lower()
        not_available_phrases = [
            "not specified", "not available", "n/a", "na", "",
            "non disponible", "non spécifié",
            "nicht verfügbar", "nicht angegeben",
            "nem elérhető", "nem megadva",
            "unknown", "inconnu", "unbekannt", "ismeretlen",
            "none", "null", "-", "--", "—"
        ]

        if (val_lower in not_available_phrases or
                val in ["N/A", "NA"] or
                val_lower.startswith(("not ", "non ", "nem ", "nicht ", "no ", "n/a"))):
            return "Not available"

        return val

    def _empty_result(self, error: str = "", raw_response: str = "") -> Dict[str, Any]:
        """Return empty result structure with error info"""
        result = {
            "allergens": {k: False for k in ["gluten", "egg", "crustaceans", "fish",
                                             "peanut", "soy", "milk", "tree_nuts",
                                             "celery", "mustard"]},
            "nutritional_values": {k: "Not available" for k in ["energy", "fat",
                                                                "carbohydrate", "sugar",
                                                                "protein", "sodium"]},
            "metadata": {"per_100g": True, "language_detected": "unknown", "confidence": "low"}
        }
        if error:
            result["error"] = error
        if raw_response:
            result["raw_response"] = raw_response
        return result

    def analyze(self, pdf_bytes: bytes, filename: str = "uploaded.pdf",
                language: str = "en") -> Dict[str, Any]:
        """
        Main analysis method: extract text from PDF and parse with LLM.

        Args:
            pdf_bytes: PDF file contents as bytes
            filename: Original filename
            language: User-selected language code

        Returns:
            Dictionary with extracted data and metadata
        """
        try:
            if not pdf_bytes:
                raise ValueError("Empty PDF bytes provided")

            logger.info("🔍 Analyze PDF bytes for file=%s language=%s size=%d bytes",
                        filename, language, len(pdf_bytes))

            # Extract text
            text, ocr_used = self.extract_text_from_pdf(pdf_bytes)

            # LLM extraction
            extracted = self.extract_data_from_text(text)

            # Attach metadata
            extracted.setdefault("metadata", {})
            extracted["metadata"].update({
                "ocr_used": ocr_used,
                "language_selected": language,
                "file_name": filename,
                "extracted_text_length": len(text)
            })

            return extracted

        except Exception as e:
            logger.exception("❌ analyze failed: %s", e)
            result = self._empty_result(error=str(e))
            result["metadata"].update({
                "ocr_used": False,
                "language_selected": language,
                "file_name": filename
            })
            return result