import { useTranslation } from 'react-i18next';

export default function ProgressBar({ progress }) {
  const { t } = useTranslation();

  return (
    <div style={{ width: '100%', margin: '20px 0' }}>
      <div
        style={{
          height: '12px',
          width: '100%',
          background: '#e9ecef',
          borderRadius: '6px',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            height: '100%',
            width: `${progress}%`,
            background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            transition: 'width 0.3s ease',
          }}
        ></div>
      </div>
      <p style={{ textAlign: 'center', marginTop: '10px', color: '#6c757d' }}>
        {t('analyzing')} {progress}%
      </p>
    </div>
  );
}
