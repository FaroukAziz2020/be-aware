import AllergensDisplay from './AllergensDisplay.jsx';
import NutritionDisplay from './NutritionDisplay.jsx';
import { forwardRef } from 'react';
import { useTranslation } from 'react-i18next';

const ResultSection = forwardRef(({ result, onDownloadPDF }, ref) => {
  const { t } = useTranslation();
  const allergens = result?.data?.allergens || {};
  const hasAllergens = Object.values(allergens).some(a => a === true);

  return (
    <div ref={ref} className="results">
      <div className="result-header">
        <h2>{t('report_title')}</h2>
      </div>

      <div className="results-grid">
        {/* 🧩 Allergens Section */}
        <div className={`result-section allergens-card ${hasAllergens ? 'danger' : 'safe'}`}>
          <AllergensDisplay allergens={allergens} />
        </div>

        {/* 🍎 Nutrition Section */}
        <div className="result-section nutrition-card">
          <h3>{t('nutrition')}</h3>
          <NutritionDisplay nutritional={result.data.nutritional_values} />
        </div>
      </div>

      {/* 💾 Download PDF Button */}
      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <button className="upload-button" onClick={onDownloadPDF}>
          {t('download_report')}
        </button>
      </div>
    </div>
  );
});

export default ResultSection;
