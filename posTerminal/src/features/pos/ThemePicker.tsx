import { useState } from "react";
import { applyTheme, customise } from "../../theme/applyTheme";

export default function ThemePicker({ themes, allowCustom, onPick, onClose }: {
  themes: any[]; allowCustom: boolean;
  onPick: (id: string) => void; onClose: () => void;
}) {
  const [sel, setSel] = useState<any | null>(null);
  const [brand, setBrand] = useState("");
  const [accent, setAccent] = useState("");
  const [name, setName] = useState("");

  function saveCustom() {
    const body = new URLSearchParams({
      theme_name: name, base: sel.base || "warm",
      brand: brand || sel.brand, brand_deep: sel.brand_deep,
      accent: accent || sel.accent, accent_deep: sel.accent_deep, make_active: "1",
    });
    fetch(`/api/method/alphax_pos.alphax_pos.api.boot.save_custom_theme`, {
      method: "POST", credentials: "include",
      headers: { "Content-Type": "application/x-www-form-urlencoded",
                 "X-Frappe-CSRF-Token": (window as any).csrf_token || "" },
      body,
    }).then(() => onClose());
  }
  return (
    <div onClick={onClose} style={overlay}>
      <div onClick={(e) => e.stopPropagation()} style={sheet}>
        <h3 style={{ fontSize: 16, fontWeight: 800, marginBottom: 12 }}>Choose a theme</h3>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(150px,1fr))", gap: 10 }}>
          {themes.map((t) => (
            <button key={t.id}
              onMouseEnter={() => applyTheme(t.tokens)}
              onClick={() => {
                applyTheme(t.tokens);
                if (allowCustom) { setSel(t); setBrand(t.brand); setAccent(t.accent); }
                else onPick(t.id);
              }}
              style={{ textAlign: "start", border: "1px solid var(--border)", borderRadius: 12,
                overflow: "hidden", background: "var(--surface)", cursor: "pointer", padding: 0 }}>
              <div style={{ height: 44, display: "flex" }}>
                <span style={{ flex: 2, background: t.brand }} />
                <span style={{ flex: 1, background: t.accent }} />
                <span style={{ flex: 1, background: t.tokens["--canvas"] }} />
              </div>
              <div style={{ padding: "8px 10px" }}>
                <div style={{ fontWeight: 700, fontSize: 12.5 }}>{t.name}</div>
                <div style={{ fontSize: 10.5, color: "var(--ink-faint)" }}>{t.vertical}</div>
              </div>
            </button>
          ))}
        </div>
        {allowCustom && sel && (
          <div style={{ marginTop: 14, display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
            <span style={{ fontSize: 12, color: "var(--ink-muted)" }}>Customise:</span>
            <label style={{ fontSize: 12 }}>Brand
              <input type="color" defaultValue={sel.brand}
                onChange={(e) => { setBrand(e.target.value); applyTheme(customise(sel.tokens, e.target.value, accent)); }}
                style={{ marginInlineStart: 6, verticalAlign: "middle" }} /></label>
            <label style={{ fontSize: 12 }}>Accent
              <input type="color" defaultValue={sel.accent}
                onChange={(e) => { setAccent(e.target.value); applyTheme(customise(sel.tokens, brand, e.target.value)); }}
                style={{ marginInlineStart: 6, verticalAlign: "middle" }} /></label>
            <input placeholder="My brand theme" value={name} onChange={(e) => setName(e.target.value)}
              style={{ height: 34, padding: "0 10px", borderRadius: 9, border: "1px solid var(--border)",
                background: "var(--surface)", color: "var(--ink)", fontSize: 12, marginInlineStart: "auto" }} />
            <button disabled={!name} onClick={saveCustom}
              style={{ height: 34, padding: "0 14px", borderRadius: 9, fontWeight: 700, fontSize: 12,
                border: "none", cursor: name ? "pointer" : "default",
                background: name ? "var(--brand)" : "var(--surface-3)",
                color: name ? "var(--brand-contrast)" : "var(--ink-faint)" }}>Save theme</button>
            <button onClick={() => onPick(sel.id)}
              style={{ height: 34, padding: "0 14px", borderRadius: 9, fontWeight: 700, fontSize: 12,
                border: "1px solid var(--border)", background: "var(--surface)", color: "var(--ink)",
                cursor: "pointer" }}>Apply preset</button>
          </div>
        )}
      </div>
    </div>
  );
}
const overlay: React.CSSProperties = { position: "fixed", inset: 0, background: "rgba(0,0,0,.4)",
  display: "grid", placeItems: "center", zIndex: 50 };
const sheet: React.CSSProperties = { background: "var(--surface)", borderRadius: 18, padding: 20,
  width: "min(720px,92vw)", maxHeight: "84vh", overflow: "auto", boxShadow: "var(--shadow)" };
