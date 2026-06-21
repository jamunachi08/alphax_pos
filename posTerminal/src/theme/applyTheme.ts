export type ThemeTokens = Record<string, string>;

/** Write a theme's tokens onto :root so every component re-skins instantly. */
export function applyTheme(tokens: ThemeTokens, overrides: ThemeTokens = {}) {
  const root = document.documentElement;
  const merged = { ...tokens, ...overrides };
  for (const [k, v] of Object.entries(merged)) root.style.setProperty(k, v);
}

/** Light tweak helper: customise brand/accent on top of a preset. */
export function customise(base: ThemeTokens, brand?: string, accent?: string): ThemeTokens {
  const surface = base["--surface"] || "#fff";
  const out = { ...base };
  if (brand) {
    out["--brand"] = brand;
    out["--brand-tint"] = `color-mix(in srgb, ${brand} 12%, ${surface})`;
  }
  if (accent) {
    out["--accent"] = accent;
    out["--accent-tint"] = `color-mix(in srgb, ${accent} 16%, ${surface})`;
  }
  return out;
}
