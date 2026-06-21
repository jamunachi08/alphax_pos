import { useEffect, useState } from "react";
import { applyTheme } from "./applyTheme";

const BASE = "/api/method/alphax_pos.alphax_pos.api.boot";

export interface Boot {
  branding: any;
  theme: { id: string; name: string; tokens: Record<string, string> };
  themes: any[];
  session?: any;
}

/** One call on load → white-label branding + active theme. */
export function useBoot() {
  const [boot, setBoot] = useState<Boot | null>(null);
  useEffect(() => {
    fetch(`${BASE}.get_boot`, { credentials: "include" })
      .then((r) => r.json())
      .then((d) => {
        const b = d.message as Boot;
        if (b?.theme?.tokens) applyTheme(b.theme.tokens);
        if (b?.branding?.default_language === "ar") {
          document.documentElement.dir = "rtl";
          document.documentElement.lang = "ar";
        }
        document.title = b?.branding?.brand_name || "POS";
        setBoot(b);
      })
      .catch(() => setBoot(null));
  }, []);
  return boot;
}
