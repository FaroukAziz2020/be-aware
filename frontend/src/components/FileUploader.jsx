import { useTranslation } from 'react-i18next';
import { useEffect, useState } from 'react';

export default function FileUploader({ file, loading, onFileChange, onUpload }) {
  const { t, i18n } = useTranslation();
  const [labelText, setLabelText] = useState(t('choose_pdf'));

  // ✅ re-run when the language changes
  useEffect(() => {
    setLabelText(t('choose_pdf'));
  }, [i18n.language, t]);

  return (
    <div className="upload-section">
      <div className="file-input-wrapper">
        <input
          type="file"
          id="file-input"
          accept=".pdf"
          onChange={onFileChange}
          disabled={loading}
        />
        <label htmlFor="file-input" className="file-input-label">
          📄 {file ? file.name : labelText}
        </label>
      </div>

      <button
        className="upload-button"
        onClick={onUpload}
        disabled={!file || loading}
      >
        {loading ? (
          <>
            <span className="spinner"></span> {t('analyzing')}
          </>
        ) : (
          t('upload_button')
        )}
      </button>
    </div>
  );
}
