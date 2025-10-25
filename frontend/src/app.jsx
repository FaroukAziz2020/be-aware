import { useState, useRef, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import { useTranslation } from 'react-i18next';
import LanguageSelector from './components/LanguageSelector.jsx';
import FileUploader from './components/FileUploader.jsx';
import ProgressBar from './components/ProgressBar.jsx';
import ResultSection from './components/ResultSection.jsx';
import ThemeToggle from './components/ThemeToggle.jsx';
import './ThemeToggle.css';
import './app.css';

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const resultRef = useRef(null);
  const { t, i18n } = useTranslation();
  const [language, setLanguage] = useState('en');

  // 🌓 Theme State
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => (prev === 'light' ? 'dark' : 'light'));

  // ✅ Fixed: Base URL without /upload
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

  const handleLanguageChange = (lang) => {
    setLanguage(lang);
    i18n.changeLanguage(lang);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setFile(null);
      setError('Please select a valid PDF file');
      toast.error('Invalid file type. Please select a PDF.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError(t('no_file_selected'));
      toast.error(t('no_file_selected'));
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language); // ✅ Added language parameter

    try {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', `${API_URL}/upload`, true); // ✅ Fixed: Added /upload endpoint

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          const percent = Math.round((e.loaded * 100) / e.total);
          setProgress(percent);
        }
      };

      xhr.onload = () => {
        setLoading(false);
        if (xhr.status >= 200 && xhr.status < 300) {
          const data = JSON.parse(xhr.responseText);
          setResult(data);
          toast.success(t('analysis_complete'));
          setTimeout(() => resultRef.current?.scrollIntoView({ behavior: 'smooth' }), 400);
        } else {
          const errData = JSON.parse(xhr.responseText);
          setError(errData.detail || t('analysis_failed'));
          toast.error(t('analysis_failed'));
        }
      };

      xhr.onerror = () => {
        setLoading(false);
        setError(t('network_error'));
        toast.error(t('network_error'));
      };

      xhr.send(formData);
    } catch (err) {
      setLoading(false);
      setError(t('unexpected_error'));
      toast.error(t('unexpected_error'));
    }
  };

  const handleDownloadPDF = async () => {
    if (!result?.data) return;
    try {
      const response = await fetch(`${API_URL}/generate-pdf`, { // ✅ Fixed: Correct endpoint
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...result.data,
          language: language
        }),
      });

      if (!response.ok) {
        toast.error(t('pdf_failed'));
        return;
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${result.filename}_aware_report.pdf`;
      link.click();
      URL.revokeObjectURL(url);
      toast.success(t('pdf_downloaded'));
    } catch {
      toast.error(t('pdf_failed'));
    }
  };

  return (
    <div className="app">
      <ToastContainer position="top-right" autoClose={3000} theme="colored" />

      <div className="container">
        <header className="header">
          <div className="top-bar">
            <div className="left-controls">
              <ThemeToggle />
            </div>

            <div className="right-controls">
              <LanguageSelector language={language} onChange={handleLanguageChange} />
            </div>
          </div>

          <svg className="logo" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" fill="#4facfe" stroke="white" strokeWidth="3" />
            <path d="M30 50 Q50 30 70 50 Q50 70 30 50" stroke="white" strokeWidth="3" fill="none" />
            <circle cx="50" cy="45" r="8" fill="white" />
            <text x="50" y="75" fontSize="20" textAnchor="middle" fill="white" fontWeight="bold">!</text>
          </svg>

          <h1>{t('title')}</h1>
          <p>{t('subtitle')}</p>
        </header>

        <FileUploader
          file={file}
          loading={loading}
          onFileChange={handleFileChange}
          onUpload={handleUpload}
        />

        {loading && <ProgressBar progress={progress} />}

        {error && (
          <div className="error-message">
            <strong>❌ Alert:</strong> {error}
          </div>
        )}

        {result && result.data && !result.data.error && (
          <ResultSection
            ref={resultRef}
            result={result}
            onDownloadPDF={handleDownloadPDF}
          />
        )}
      </div>

      <footer className="footer">
        <p>{t('footer')}</p>
      </footer>
    </div>
  );
}