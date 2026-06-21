import { useEffect, useMemo, useRef, useState } from "react";
import type { Boot } from "../../theme/useBoot";
import { applyTheme } from "../../theme/applyTheme";
import { PRESET_THEMES } from "../../theme/themes";
import ThemePicker from "./ThemePicker";
import PaymentModal from "./PaymentModal";

const API = "/api/method/alphax_pos.alphax_pos.api";

interface Cat { name: string; category_name: string; category_name_ar?: string; color?: string; icon?: string; }
interface Item {
  name: string; item_label: string; item_label_ar?: string; category: string;
  price: number; emoji?: string; image?: string; is_86?: number; has_modifiers?: number;
}
interface Line {
  key: string; menu_item: string; item_label: string; item_label_ar?: string;
  rate: number; qty: number; emoji?: string;
}

/* ---- Demo catalog (shown until a menu + profile are configured) ---- */
const DEMO_CATS: Cat[] = [
  { name: "Hot Coffee", category_name: "Hot Coffee", color: "#7a4a2b" },
  { name: "Cold Coffee", category_name: "Cold Coffee", color: "#2f6fb0" },
  { name: "Tea", category_name: "Tea", color: "#1e9e6a" },
  { name: "Bakery", category_name: "Bakery", color: "#d98c00" },
  { name: "Desserts", category_name: "Desserts", color: "#b23b7a" },
  { name: "Savory", category_name: "Savory", color: "#9a6212" },
];
const DEMO_ITEMS: Item[] = [
  { name: "Cappuccino", item_label: "Cappuccino", item_label_ar: "كابتشينو", category: "Hot Coffee", price: 16, emoji: "☕", has_modifiers: 1 },
  { name: "Flat White", item_label: "Flat White", item_label_ar: "فلات وايت", category: "Hot Coffee", price: 18, emoji: "☕", has_modifiers: 1 },
  { name: "Latte", item_label: "Latte", item_label_ar: "لاتيه", category: "Hot Coffee", price: 17, emoji: "☕", has_modifiers: 1 },
  { name: "Espresso", item_label: "Espresso", item_label_ar: "إسبريسو", category: "Hot Coffee", price: 12, emoji: "☕" },
  { name: "Spanish Latte", item_label: "Spanish Latte", item_label_ar: "سبانيش لاتيه", category: "Hot Coffee", price: 19, emoji: "☕", has_modifiers: 1 },
  { name: "Turkish Coffee", item_label: "Turkish Coffee", item_label_ar: "قهوة تركية", category: "Hot Coffee", price: 14, emoji: "☕" },
  { name: "Saudi Coffee", item_label: "Saudi Coffee", item_label_ar: "قهوة عربية", category: "Hot Coffee", price: 14, emoji: "🫖" },
  { name: "Iced Latte", item_label: "Iced Latte", item_label_ar: "آيس لاتيه", category: "Cold Coffee", price: 18, emoji: "🧊" },
  { name: "Cold Brew", item_label: "Cold Brew", item_label_ar: "كولد برو", category: "Cold Coffee", price: 20, emoji: "🧊" },
  { name: "Green Tea", item_label: "Green Tea", item_label_ar: "شاي أخضر", category: "Tea", price: 10, emoji: "🍵" },
  { name: "Croissant", item_label: "Croissant", item_label_ar: "كرواسون", category: "Bakery", price: 12, emoji: "🥐" },
  { name: "Cheesecake", item_label: "Cheesecake", item_label_ar: "تشيز كيك", category: "Desserts", price: 22, emoji: "🍰" },
];

const STR: Record<string, { en: string; ar: string }> = {
  dine: { en: "Dine-in", ar: "صالة" }, take: { en: "Takeaway", ar: "سفري" }, deliv: { en: "Delivery", ar: "توصيل" },
  search: { en: "Search items…", ar: "ابحث عن صنف…" }, menu: { en: "MENU", ar: "القائمة" },
  tap: { en: "Tap an item to add it to the order", ar: "اضغط على صنف لإضافته للطلب" },
  order: { en: "Order", ar: "طلب" }, subtotal: { en: "Subtotal", ar: "المجموع" },
  vat: { en: "VAT", ar: "ضريبة" }, total: { en: "Total", ar: "الإجمالي" }, pay: { en: "Pay", ar: "دفع" },
  hold: { en: "Hold", ar: "تعليق" }, release: { en: "Release", ar: "استرجاع" }, last: { en: "Last invoice", ar: "آخر فاتورة" },
  ret: { en: "Sales return", ar: "مرتجع" }, void: { en: "Void", ar: "إلغاء" }, more: { en: "More", ar: "المزيد" },
};

export default function POSScreen({ boot }: { boot: Boot }) {
  const { branding } = boot;
  const session = boot.session || null;
  const vatRate = session?.vat_rate ?? 15;
  const symbol = branding.currency_symbol || "SAR";

  const [lang, setLang] = useState<"en" | "ar">(branding.default_language === "ar" ? "ar" : "en");
  const t = (k: string) => STR[k]?.[lang] ?? k;

  const [cats, setCats] = useState<Cat[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [demo, setDemo] = useState(false);
  const [activeCat, setActiveCat] = useState<string>("");
  const [orderType, setOrderType] = useState<"dine_in" | "takeaway" | "delivery">("dine_in");
  const [query, setQuery] = useState("");

  const [cart, setCart] = useState<Line[]>([]);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [payOpen, setPayOpen] = useState(false);
  const [paidBanner, setPaidBanner] = useState<string | null>(null);
  const orderNoRef = useRef<string | undefined>(undefined);
  const [orderNum] = useState(() => 1000 + Math.floor(Math.random() * 9000));

  useEffect(() => {
    const url = session?.pos_profile
      ? `${API}/menu.tree?pos_profile=${encodeURIComponent(session.pos_profile)}`
      : `${API}/menu.tree`;
    fetch(url, { credentials: "include" })
      .then((r) => r.json())
      .then((d) => {
        const m = d.message || {};
        const its: Item[] = m.items || [];
        if (its.length) {
          setCats(m.categories || []); setItems(its); setDemo(false);
          setActiveCat((m.categories?.[0]?.name) || its[0]?.category || "");
        } else { useDemo(); }
      })
      .catch(useDemo);
    function useDemo() {
      setCats(DEMO_CATS); setItems(DEMO_ITEMS); setDemo(true);
      setActiveCat(DEMO_CATS[0].name);
    }
  }, [session?.pos_profile]);

  useEffect(() => {
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.documentElement.lang = lang;
  }, [lang]);

  const countByCat = useMemo(() => {
    const c: Record<string, number> = {};
    items.forEach((i) => { c[i.category] = (c[i.category] || 0) + 1; });
    return c;
  }, [items]);

  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    return items.filter((i) =>
      (q ? (i.item_label.toLowerCase().includes(q) || (i.item_label_ar || "").includes(q))
         : i.category === activeCat));
  }, [items, activeCat, query]);

  const subtotal = useMemo(() => cart.reduce((s, l) => s + l.rate * l.qty, 0), [cart]);
  const vat = useMemo(() => subtotal * vatRate / 100, [subtotal, vatRate]);
  const total = subtotal + vat;

  function addItem(it: Item) {
    if (it.is_86) return;
    setPaidBanner(null);
    setCart((c) => {
      const i = c.findIndex((l) => l.menu_item === it.name);
      if (i >= 0) { const n = [...c]; n[i] = { ...n[i], qty: n[i].qty + 1 }; return n; }
      return [...c, { key: it.name + ":" + Date.now(), menu_item: it.name, item_label: it.item_label,
        item_label_ar: it.item_label_ar, rate: it.price, qty: 1, emoji: it.emoji }];
    });
  }
  const setQty = (key: string, d: number) => setCart((c) =>
    c.map((l) => l.key === key ? { ...l, qty: Math.max(0, l.qty + d) } : l).filter((l) => l.qty > 0));
  const clearCart = () => { setCart([]); orderNoRef.current = undefined; };

  async function startPay() {
    if (!cart.length) return;
    if (session?.pos_profile) {
      try {
        const r = await fetch(`${API}/order.create`, {
          method: "POST", credentials: "include",
          headers: { "Content-Type": "application/json", "X-Frappe-CSRF-Token": (window as any).csrf_token || "" },
          body: JSON.stringify({ order: JSON.stringify({
            pos_profile: session.pos_profile, terminal: session.terminal, order_type: orderType,
            customer: session.default_customer, vat_rate: vatRate,
            lines: cart.map((l) => ({ menu_item: l.menu_item, item_label: l.item_label, qty: l.qty, rate: l.rate })),
          }) }),
        });
        const d = await r.json();
        orderNoRef.current = d.message?.order_no;
      } catch { /* fall through to demo pay */ }
    }
    setPayOpen(true);
  }
  function onPaid(res: any) {
    const change = res?.change ? ` · change ${symbol} ${Number(res.change).toFixed(2)}` : "";
    setPaidBanner(`Paid ${symbol} ${Number(res?.paid ?? total).toFixed(2)}${change}`);
    clearCart();
  }

  function pickTheme(themeId: string) {
    const th = PRESET_THEMES.find((x) => x.id === themeId);
    if (th) applyTheme(th.tokens as Record<string, string>);
    fetch(`${API}/boot.set_active_theme?theme_id=${themeId}`, { method: "POST", credentials: "include",
      headers: { "X-Frappe-CSRF-Token": (window as any).csrf_token || "" } });
    setPickerOpen(false);
  }

  const outletLabel = lang === "ar"
    ? (session?.outlet_name_ar || session?.outlet_name || "")
    : (session?.outlet_name || "");

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "var(--canvas)" }}>
      {/* ===== Header ===== */}
      <header style={hdr}>
        <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
          {branding.logo_light
            ? <img src={branding.logo_light} alt="" style={{ height: 40 }} />
            : <div style={logoBox}>α</div>}
          <div style={{ lineHeight: 1.15 }}>
            <div style={{ fontWeight: 800, fontSize: 16 }}>{branding.brand_name}</div>
            <div style={{ fontSize: 12, color: "var(--ink-muted)" }}>
              {outletLabel ? `${outletLabel}` : "Riyadh"}
            </div>
          </div>
          {demo && <span style={demoBadge}>DEMO</span>}
        </div>

        {/* order-type segmented */}
        <div style={seg}>
          {([["dine_in", "🍽", t("dine")], ["takeaway", "🛍", t("take")], ["delivery", "🛵", t("deliv")]] as const)
            .map(([k, ic, lbl]) => (
            <button key={k} onClick={() => setOrderType(k as any)} style={segBtn(orderType === k)}>
              <span style={{ fontSize: 15 }}>{ic}</span>{lbl}
            </button>
          ))}
        </div>

        <div style={{ flex: 1, position: "relative", maxWidth: 460 }}>
          <span style={{ position: "absolute", insetInlineStart: 14, top: 11, color: "var(--ink-faint)" }}>🔍</span>
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={t("search")}
            style={searchBox} />
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <button onClick={() => setLang(lang === "ar" ? "en" : "ar")} style={pill}>
            {lang === "ar" ? "EN" : "العربية"}
          </button>
          {branding.allow_theme_switch && (
            <button onClick={() => setPickerOpen(true)} style={pill}>🎨</button>
          )}
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginInlineStart: 4 }}>
            <div style={avatar}>{(session?.cashier || "U").split(" ").map((s: string) => s[0]).slice(0, 2).join("")}</div>
            <div style={{ lineHeight: 1.15 }}>
              <div style={{ fontWeight: 700, fontSize: 13 }}>{session?.cashier || "Cashier"}</div>
              <div style={{ fontSize: 11, color: "var(--ink-muted)" }}>
                {session?.shift ? `Shift ${session.shift}` : "No open shift"}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* ===== Body ===== */}
      <div style={{ flex: 1, display: "grid", gridTemplateColumns: "210px 1fr 360px", minHeight: 0 }}>
        {/* Sidebar */}
        <aside style={sidebar}>
          <div style={{ fontSize: 11, fontWeight: 800, letterSpacing: ".8px", color: "var(--ink-faint)", padding: "4px 8px 10px" }}>
            {t("menu")}
          </div>
          {cats.map((c) => {
            const on = c.name === activeCat && !query;
            return (
              <button key={c.name} onClick={() => { setActiveCat(c.name); setQuery(""); }} style={catRow(on)}>
                <span style={{ width: 9, height: 9, borderRadius: 9, background: c.color || "var(--brand)" }} />
                <span style={{ flex: 1, textAlign: "start", fontWeight: on ? 700 : 600 }}>
                  {lang === "ar" ? (c.category_name_ar || c.category_name) : c.category_name}
                </span>
                <span style={{ fontSize: 12, color: "var(--ink-faint)" }}>{countByCat[c.name] || 0}</span>
              </button>
            );
          })}
        </aside>

        {/* Catalog */}
        <main style={{ padding: "18px 20px", overflowY: "auto", minHeight: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 4 }}>
            <h2 style={{ fontSize: 22, fontWeight: 800 }}>{query ? `“${query}”` : activeCat}</h2>
            {session?.features?.kot && <span style={station}>● Barista station</span>}
          </div>
          <p style={{ color: "var(--ink-muted)", fontSize: 13, marginBottom: 14 }}>{t("tap")}</p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(180px,1fr))", gap: 14 }}>
            {shown.map((it) => (
              <button key={it.name} onClick={() => addItem(it)} disabled={!!it.is_86} style={card(!!it.is_86)}>
                {it.has_modifiers ? <span style={modsBadge}>+ mods</span> : null}
                <div style={thumb}>
                  {it.image ? <img src={it.image} alt="" style={{ width: 46, height: 46, borderRadius: 12, objectFit: "cover" }} />
                    : <span style={{ fontSize: 30 }}>{it.emoji || "🍽"}</span>}
                </div>
                <div style={{ fontWeight: 700, fontSize: 14, marginTop: 8 }}>{it.item_label}</div>
                {it.item_label_ar && <div style={{ fontSize: 12, color: "var(--ink-muted)" }}>{it.item_label_ar}</div>}
                <div style={{ marginTop: 6, color: "var(--brand-deep)", fontWeight: 800 }}>
                  <span style={{ fontSize: 11, color: "var(--ink-faint)" }}>{symbol} </span>{it.price.toFixed(2)}
                </div>
                {it.is_86 ? <span style={{ fontSize: 11, color: "var(--neg)", fontWeight: 700 }}>86 / out</span> : null}
              </button>
            ))}
          </div>
        </main>

        {/* Order panel */}
        <section style={orderPane}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 16px 8px" }}>
            <div style={{ fontSize: 18, fontWeight: 800 }}>{t("order")} <span style={{ color: "var(--ink-faint)" }}>#{orderNum}</span></div>
            {orderType === "dine_in" && session?.features?.tables !== false &&
              <span style={tableBadge}>🪑 Table 12</span>}
          </div>

          <div style={{ flex: 1, overflowY: "auto", padding: "4px 12px", minHeight: 0 }}>
            {cart.length === 0 ? (
              <div style={{ height: "100%", display: "grid", placeItems: "center", color: "var(--ink-faint)", textAlign: "center" }}>
                <div>
                  <div style={{ fontSize: 34, marginBottom: 8 }}>🧾</div>
                  <div style={{ fontSize: 13 }}>{t("tap")}</div>
                </div>
              </div>
            ) : cart.map((l) => (
              <div key={l.key} style={lineRow}>
                <div style={qtyBox}>
                  <button onClick={() => setQty(l.key, -1)} style={qtyBtn}>−</button>
                  <span style={{ minWidth: 18, textAlign: "center", fontWeight: 800 }}>{l.qty}</span>
                  <button onClick={() => setQty(l.key, +1)} style={qtyBtn}>+</button>
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 700, fontSize: 14, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {lang === "ar" ? (l.item_label_ar || l.item_label) : l.item_label}
                  </div>
                  <div style={{ fontSize: 12, color: "var(--ink-muted)" }}>{symbol} {l.rate.toFixed(2)}</div>
                </div>
                <div style={{ fontWeight: 800 }}>{(l.rate * l.qty).toFixed(2)}</div>
              </div>
            ))}
          </div>

          {paidBanner && <div style={paidBox}>✓ {paidBanner}</div>}

          {/* totals */}
          <div style={{ padding: "10px 16px", borderTop: "1px solid var(--border)" }}>
            <Row label={t("subtotal")} value={`${symbol} ${subtotal.toFixed(2)}`} />
            <Row label={`${t("vat")} ${vatRate}%`} value={`${symbol} ${vat.toFixed(2)}`} />
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginTop: 8 }}>
              <span style={{ fontWeight: 800, fontSize: 20 }}>{t("total")}</span>
              <span style={{ fontWeight: 800, fontSize: 22, color: "var(--pos)" }}>
                <span style={{ fontSize: 12, color: "var(--ink-faint)" }}>{symbol} </span>{total.toFixed(2)}
              </span>
            </div>
          </div>

          {/* secondary actions */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, padding: "0 12px 8px" }}>
            {[["⏸", t("hold")], ["▶", t("release")], ["🧾", t("last")], ["↩", t("ret")], ["⛔", t("void")], ["⋯", t("more")]]
              .map(([ic, lbl], i) => (
              <button key={i} onClick={() => { if (lbl === t("void")) clearCart(); }} style={actBtn(lbl === t("void"))}>
                <span style={{ fontSize: 16 }}>{ic}</span><span style={{ fontSize: 11 }}>{lbl}</span>
              </button>
            ))}
          </div>

          {/* Pay */}
          <button onClick={startPay} disabled={!cart.length} style={payBtn(!!cart.length)}>
            <span>💳 {t("pay")}</span>
            <span>{symbol} {total.toFixed(2)}</span>
          </button>
        </section>
      </div>

      {pickerOpen && <ThemePicker themes={PRESET_THEMES as any} allowCustom={branding.allow_theme_custom}
        onPick={pickTheme} onClose={() => setPickerOpen(false)} />}
      {payOpen && <PaymentModal posProfile={session?.pos_profile || "Demo"} total={total}
        orderNo={orderNoRef.current} onPaid={onPaid} onClose={() => setPayOpen(false)} />}
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, color: "var(--ink-muted)", marginBottom: 4 }}>
      <span>{label}</span><span style={{ color: "var(--ink)", fontWeight: 600 }}>{value}</span>
    </div>
  );
}

/* ---------- styles ---------- */
const hdr: React.CSSProperties = { display: "flex", alignItems: "center", gap: 14, padding: "10px 16px",
  background: "var(--surface)", borderBottom: "1px solid var(--border)" };
const logoBox: React.CSSProperties = { width: 42, height: 42, borderRadius: 13, background: "var(--brand)",
  color: "var(--brand-contrast)", display: "grid", placeItems: "center", fontWeight: 800, fontSize: 20 };
const demoBadge: React.CSSProperties = { fontSize: 11, fontWeight: 800, color: "var(--accent-deep)",
  background: "var(--accent-tint)", padding: "3px 8px", borderRadius: 8, letterSpacing: ".5px" };
const seg: React.CSSProperties = { display: "flex", gap: 4, background: "var(--surface-2)", padding: 4, borderRadius: 13 };
function segBtn(on: boolean): React.CSSProperties {
  return { display: "flex", alignItems: "center", gap: 6, height: 38, padding: "0 14px", borderRadius: 10,
    border: "none", cursor: "pointer", fontWeight: 700, fontSize: 13,
    background: on ? "var(--surface)" : "transparent", color: on ? "var(--ink)" : "var(--ink-muted)",
    boxShadow: on ? "var(--shadow)" : "none" };
}
const searchBox: React.CSSProperties = { width: "100%", height: 42, borderRadius: 12, border: "1px solid var(--border)",
  background: "var(--surface-2)", padding: "0 14px 0 38px", fontSize: 14, color: "var(--ink)", outline: "none" };
const pill: React.CSSProperties = { height: 38, padding: "0 12px", borderRadius: 11, border: "1px solid var(--border)",
  background: "var(--surface-2)", color: "var(--ink)", fontWeight: 700, fontSize: 13, cursor: "pointer" };
const avatar: React.CSSProperties = { width: 38, height: 38, borderRadius: 11, background: "var(--brand-tint)",
  color: "var(--brand-deep)", display: "grid", placeItems: "center", fontWeight: 800, fontSize: 13 };
const sidebar: React.CSSProperties = { background: "var(--surface)", borderInlineEnd: "1px solid var(--border)",
  padding: "14px 10px", overflowY: "auto", display: "flex", flexDirection: "column", gap: 4 };
function catRow(on: boolean): React.CSSProperties {
  return { display: "flex", alignItems: "center", gap: 10, height: 44, padding: "0 12px", borderRadius: 12,
    border: "none", cursor: "pointer", fontSize: 14, color: "var(--ink)",
    background: on ? "var(--brand-tint)" : "transparent" };
}
const station: React.CSSProperties = { fontSize: 12, fontWeight: 700, color: "var(--ink-muted)",
  background: "var(--surface-2)", padding: "5px 10px", borderRadius: 9 };
function card(disabled: boolean): React.CSSProperties {
  return { position: "relative", textAlign: "start", background: "var(--surface)", border: "1px solid var(--border)",
    borderRadius: 16, padding: 14, cursor: disabled ? "default" : "pointer", opacity: disabled ? 0.5 : 1,
    boxShadow: "var(--shadow)", transition: "transform .05s" };
}
const thumb: React.CSSProperties = { width: "100%", height: 74, borderRadius: 12, background: "var(--surface-2)",
  display: "grid", placeItems: "center" };
const modsBadge: React.CSSProperties = { position: "absolute", top: 8, insetInlineStart: 8, fontSize: 10, fontWeight: 800,
  color: "var(--accent-deep)", background: "var(--surface)", border: "1px solid var(--border)",
  padding: "2px 7px", borderRadius: 8 };
const orderPane: React.CSSProperties = { background: "var(--surface)", borderInlineStart: "1px solid var(--border)",
  display: "flex", flexDirection: "column", minHeight: 0 };
const tableBadge: React.CSSProperties = { fontSize: 12, fontWeight: 700, color: "var(--ink)",
  background: "var(--surface-2)", padding: "5px 10px", borderRadius: 9 };
const lineRow: React.CSSProperties = { display: "flex", alignItems: "center", gap: 10, padding: "9px 6px",
  borderBottom: "1px solid var(--border)" };
const qtyBox: React.CSSProperties = { display: "flex", alignItems: "center", gap: 6, background: "var(--surface-2)",
  borderRadius: 10, padding: "3px 6px" };
const qtyBtn: React.CSSProperties = { width: 24, height: 24, borderRadius: 7, border: "none", cursor: "pointer",
  background: "var(--surface)", color: "var(--ink)", fontWeight: 800, fontSize: 15 };
const paidBox: React.CSSProperties = { margin: "0 16px", padding: "8px 12px", borderRadius: 10, fontWeight: 700,
  fontSize: 13, color: "var(--pos)", background: "var(--brand-tint)" };
function actBtn(neg: boolean): React.CSSProperties {
  return { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 3, height: 52,
    borderRadius: 12, border: "1px solid var(--border)", cursor: "pointer", background: "var(--surface-2)",
    color: neg ? "var(--neg)" : "var(--ink)", fontWeight: 600 };
}
function payBtn(active: boolean): React.CSSProperties {
  return { display: "flex", alignItems: "center", justifyContent: "space-between", margin: 12, height: 60,
    padding: "0 22px", borderRadius: 15, border: "none", cursor: active ? "pointer" : "default", fontWeight: 800, fontSize: 17,
    background: active ? "var(--brand)" : "var(--surface-3)", color: active ? "var(--brand-contrast)" : "var(--ink-faint)" };
}
