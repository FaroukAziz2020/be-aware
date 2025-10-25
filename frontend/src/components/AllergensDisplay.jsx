import { useTranslation } from 'react-i18next';

export default function AllergensDisplay({ allergens }) {
  const { t } = useTranslation();
 
  const allergenList = [
    { key: 'gluten', icon: '🌾' },
    { key: 'egg', icon: '🥚' },
    { key: 'crustaceans', icon: '🦐' },
    { key: 'fish', icon: '🐟' },
    { key: 'peanut', icon: '🥜' },
    { key: 'soy', icon: '🫘' },
    { key: 'milk', icon: '🥛' },
    { key: 'tree_nuts', icon: '🌰' },
    { key: 'celery', icon: '🥬' },
    { key: 'mustard', icon: '🌭' },
  ];

  const detected = allergenList.filter(({ key }) => allergens[key]);

  return (
    <div className="allergen-container result-section">
      <h3>
        ⚠️ {t('allergens_title')}
      </h3>
     
      {detected.length > 0 ? (
        <div className="allergen-cards">
          {allergenList.map(({ key, icon }) => (
            <div
              key={key}
              className={`allergen-card ${allergens[key] ? 'present' : 'absent'}`}
            >
              <span className="allergen-icon">{icon}</span>
              <span className="allergen-name">{t(`allergen_${key}`)}</span>
              <span className="allergen-status">
                {allergens[key] ? '✓' : '✗'}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-allergens-card">
          <p>✅ {t('safety_note_no_allergens')}</p>
        </div>
      )}
    </div>
  );
}