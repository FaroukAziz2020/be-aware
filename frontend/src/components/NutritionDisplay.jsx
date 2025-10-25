import { useTranslation } from 'react-i18next';

export default function NutritionDisplay({ nutritional }) {
  const { t } = useTranslation();
 
  // Emoji mapping for better visuals 🍎
  const nutritionIcons = {
    energy: '⚡',
    fat: '🥑',
    carbohydrate: '🍞',
    sugar: '🍬',
    protein: '🍗',
    sodium: '🧂',
  };

  // Key mapping: backend key -> translation key
  const nutritionKeyMap = {
    energy: 'nutrition_energy',
    fat: 'nutrition_fat',
    carbohydrate: 'nutrition_carbohydrate',
    carbohydrates: 'nutrition_carbohydrates',
    sugar: 'nutrition_sugar',
    sugars: 'nutrition_sugars',
    protein: 'nutrition_protein',
    sodium: 'nutrition_sodium',
  };

  const entries = Object.entries(nutritional || {});
 
  // 🧾 No data fallback
  if (entries.length === 0) {
    return <p>📉 {t('no_nutrition_data')}</p>;
  }

  return (
    <div className="nutrition-table">
      {entries.map(([key, value]) => {
        const translationKey = nutritionKeyMap[key] || `nutrition_${key}`;
        return (
          <div key={key} className="nutrition-row">
            <span className="nutrition-label">
              {nutritionIcons[key] || '🍽️'} {t(translationKey, key)}
            </span>
            <span className="nutrition-value">
              {value && value !== 'Not available' ? value : t('not_available')}
            </span>
          </div>
        );
      })}
    </div>
  );
}