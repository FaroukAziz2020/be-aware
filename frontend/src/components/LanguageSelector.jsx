export default function LanguageSelector({ language, onChange }) {
  return (
    <div className="language-selector">
      <select
        value={language}
        onChange={(e) => onChange(e.target.value)}
        className="language-dropdown"
      >
        <option value="en">🇬🇧 English</option>
        <option value="fr">🇫🇷 Français</option>
        <option value="de">🇩🇪 Deutsch</option>
        <option value="hu">🇭🇺 Magyar</option>
      </select>
    </div>
  );
}
