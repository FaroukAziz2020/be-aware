#!/usr/bin/env bash
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu tesseract-ocr-fra tesseract-ocr-hun poppler-utils
pip install -r requirements.txt