# pdf_generator.py - PDF Report Generation
import io
import re
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generate localized PDF reports"""

    # Translations
    TRANSLATIONS = {
        "en": {
            "title": "Food Product Analysis Report",
            "allergens": "Allergen Information",
            "nutrition": "Nutritional Values (per 100g)",
            "col_allergen": "Allergen",
            "col_present": "Present",
            "col_nutrient": "Nutrient",
            "col_value": "Value",
            "no_allergens": "No allergens detected.",
            "no_nutrition": "No nutrition data available.",
            "not_available": "Not available",
        },
        "fr": {
            "title": "Rapport d'analyse du produit alimentaire",
            "allergens": "Informations sur les allergènes",
            "nutrition": "Valeurs nutritionnelles (pour 100g)",
            "col_allergen": "Allergène",
            "col_present": "Présent",
            "col_nutrient": "Nutriment",
            "col_value": "Valeur",
            "no_allergens": "Aucun allergène détecté.",
            "no_nutrition": "Aucune donnée nutritionnelle disponible.",
            "not_available": "Non disponible",
        },
        "de": {
            "title": "Lebensmittelanalysebericht",
            "allergens": "Allergeninformationen",
            "nutrition": "Nährwerte (pro 100g)",
            "col_allergen": "Allergen",
            "col_present": "Vorhanden",
            "col_nutrient": "Nährstoff",
            "col_value": "Wert",
            "no_allergens": "Keine Allergene festgestellt.",
            "no_nutrition": "Keine Nährwertdaten verfügbar.",
            "not_available": "Nicht verfügbar",
        },
        "hu": {
            "title": "Élelmiszertermék elemzési jelentés",
            "allergens": "Allergén információk",
            "nutrition": "Tápértékek (100 g-ra)",
            "col_allergen": "Allergén",
            "col_present": "Jelen van",
            "col_nutrient": "Tápanyag",
            "col_value": "Érték",
            "no_allergens": "Nem találtunk allergéneket.",
            "no_nutrition": "Nincsenek elérhető tápérték adatok.",
            "not_available": "Nem elérhető",
        },
    }

    # Allergen names
    ALLERGEN_LABELS = {
        "en": {
            "gluten": "Gluten", "milk": "Milk", "egg": "Egg", "soy": "Soy",
            "celery": "Celery", "mustard": "Mustard", "peanut": "Peanut",
            "tree_nuts": "Tree Nuts", "crustaceans": "Crustaceans", "fish": "Fish"
        },
        "fr": {
            "gluten": "Gluten", "milk": "Lait", "egg": "Œuf", "soy": "Soja",
            "celery": "Céleri", "mustard": "Moutarde", "peanut": "Arachide",
            "tree_nuts": "Fruits à coque", "crustaceans": "Crustacés", "fish": "Poisson"
        },
        "de": {
            "gluten": "Gluten", "milk": "Milch", "egg": "Ei", "soy": "Soja",
            "celery": "Sellerie", "mustard": "Senf", "peanut": "Erdnuss",
            "tree_nuts": "Schalenfrüchte", "crustaceans": "Krebstiere", "fish": "Fisch"
        },
        "hu": {
            "gluten": "Glutén", "milk": "Tej", "egg": "Tojás", "soy": "Szója",
            "celery": "Zeller", "mustard": "Mustár", "peanut": "Földimogyoró",
            "tree_nuts": "Diófélék", "crustaceans": "Rákfélék", "fish": "Hal"
        }
    }

    # Nutrient names
    NUTRIENT_LABELS = {
        "en": {
            "energy": "Energy", "fat": "Fat", "carbohydrate": "Carbohydrate",
            "sugar": "Sugar", "protein": "Protein", "sodium": "Sodium"
        },
        "fr": {
            "energy": "Énergie", "fat": "Matières grasses", "carbohydrate": "Glucides",
            "sugar": "Sucres", "protein": "Protéines", "sodium": "Sodium"
        },
        "de": {
            "energy": "Energie", "fat": "Fett", "carbohydrate": "Kohlenhydrate",
            "sugar": "Zucker", "protein": "Eiweiß", "sodium": "Natrium"
        },
        "hu": {
            "energy": "Energia", "fat": "Zsír", "carbohydrate": "Szénhidrát",
            "sugar": "Cukor", "protein": "Fehérje", "sodium": "Nátrium"
        }
    }

    def generate(self, payload: Dict[str, Any]) -> io.BytesIO:
        """
        Generate PDF report

        Args:
            payload: Data containing allergens, nutritional_values, and language

        Returns:
            BytesIO: PDF file bytes
        """
        lang = payload.get("language", "en")
        logger.info(f"Generating PDF with language: {lang}")

        tr = self.TRANSLATIONS.get(lang, self.TRANSLATIONS["en"])
        allergens = payload.get("allergens") or payload.get("data", {}).get("allergens", {})
        nutritional = payload.get("nutritional_values") or payload.get("data", {}).get("nutritional_values", {})

        # Build PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading2"]
        normal_style = styles["Normal"]
        symbol_style = ParagraphStyle("symbol", parent=normal_style, alignment=1, fontSize=14)

        # Title
        elements.append(Paragraph(f"📊 {tr['title']}", title_style))
        elements.append(Spacer(1, 0.4 * cm))

        # Allergens Section
        elements.append(Paragraph(f"⚠️ {tr['allergens']}", heading_style))
        if not allergens:
            elements.append(Paragraph(tr["no_allergens"], normal_style))
        else:
            allergen_table = self._build_allergen_table(allergens, lang, tr, symbol_style)
            elements.append(allergen_table)

        elements.append(Spacer(1, 0.6 * cm))

        # Nutrition Section
        elements.append(Paragraph(f"📈 {tr['nutrition']}", heading_style))
        if not nutritional:
            elements.append(Paragraph(tr["no_nutrition"], normal_style))
        else:
            nutrition_table = self._build_nutrition_table(nutritional, lang, tr)
            elements.append(nutrition_table)

        doc.build(elements)
        buffer.seek(0)

        return buffer

    def _build_allergen_table(self, allergens: Dict, lang: str, tr: Dict, symbol_style) -> Table:
        """Build allergen table"""
        data = [[tr["col_allergen"], ""]]

        for key in sorted(allergens.keys()):
            present = bool(allergens.get(key, False))
            symbol = "✓" if present else "✗"
            label = self.ALLERGEN_LABELS.get(lang, self.ALLERGEN_LABELS["en"]).get(key, key)

            data.append([
                label,
                Paragraph(f'<font color="{"green" if present else "red"}">{symbol}</font>', symbol_style)
            ])

        table = Table(data, colWidths=[8 * cm, 3 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        return table

    def _build_nutrition_table(self, nutritional: Dict, lang: str, tr: Dict) -> Table:
        """Build nutrition table"""
        data = [[tr["col_nutrient"], tr["col_value"]]]

        for key in ["energy", "fat", "carbohydrate", "sugar", "protein", "sodium"]:
            value = nutritional.get(key, tr["not_available"])

            # Normalize value
            if isinstance(value, str):
                value = self._normalize_value(value.strip(), tr)

            label = self.NUTRIENT_LABELS.get(lang, self.NUTRIENT_LABELS["en"]).get(key, key.title())
            data.append([label, value])

        table = Table(data, colWidths=[8 * cm, 4 * cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        return table

    @staticmethod
    def _normalize_value(value: str, tr: Dict) -> str:
        """Normalize nutritional value"""
        # Remove parenthetical notes
        value = re.sub(
            r'\s*\((as\s+)?salt\)|\((comme\s+)?sel\)|\((als\s+)?Salz\)|\(sóként\)',
            '', value, flags=re.IGNORECASE
        ).strip()

        # Check for "not available" phrases
        value_lower = value.lower()
        not_available_phrases = [
            "not available", "not specified", "n/a", "na", "",
            "non disponible", "non spécifié",
            "nicht verfügbar", "nicht angegeben",
            "nem elérhető", "nem megadva",
            "unknown", "inconnu", "unbekannt", "ismeretlen",
            "none", "null", "-", "--", "—"
        ]

        if (value_lower in not_available_phrases or
                value in ["N/A", "NA"] or
                value_lower.startswith(("not ", "non ", "nem ", "nicht ", "no ", "n/a"))):
            return tr["not_available"]

        return value