import { useEffect, useMemo, useState } from "react";

interface Mode { id: string; name: string; kind: string; icon?: string;
  requires_terminal?: number; requires_reference?: number; }
interface Denom { label: string; value: number; kind: string; }

export default function PaymentModal({ posProfile, total, orderNo, onPaid, onClose }: {
  posProfile: string; total: number; orderNo?: string;
  onPaid?: (r: any) => void; onClose: () => void;
}) {
  const [modes, setModes] = useState<Mode[]>([]);
  const [denoms, setDenoms] = useState<Denom[]>([]);
  const [mode, setMode] = useState<Mode | null>(null);
  const [tendered, setTendered] = useState<number>(0);
  const [showDenoms, setShowDenoms] = useState(true);

  useEffect(() => {
    fetch(`/api/method/alphax_pos.alphax_pos.api.payment.modes?pos_profile=${posProfile}`,
      { credentials: "include" }).then(r => r.json())
      .then(d => setModes(d.message?.length ? d.message : FALLBACK)).catch(() => setModes(FALLBACK));
    fetch(`/api/method/alphax_pos.alphax_pos.api.payment.denominations`, { credentials: "include" })
      .then(r => r.json()).then(d => setDenoms(d.message || DEN)).catch(() => setDenoms(DEN));
  }, [posProfile]);

  const isCash = mode?.kind === "cash";
  const change = useMemo(() => Math.max(0, tendered - total), [tendered, total]);
  const balance = useMemo(() => Math.max(0, total - tendered), [tendered, total]);

  return (
    <div onClick={onClose} style={overlay}>
      <div onClick={e => e.stopPropagation()} style={sheet}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <h3 style={{ fontSize: 16, fontWeight: 800 }}>Payment</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "var(--ink-faint)" }}>×</button>
        </div>

        {/* Total / Paid / Change strip */}
        <div style={strip}>
          <Cell label="Total bill" value={total} big />
          <Cell label="Customer paid" value={tendered} accent />
          <Cell label={change > 0 ? "Change due" : "Balance"} value={change > 0 ? change : balance}
                tone={change > 0 ? "pos" : "neg"} big />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 9, marginTop: 14 }}>
          {modes.map(m => (
            <button key={m.id} onClick={() => { setMode(m); if (m.kind !== "cash") setTendered(total); }}
              style={modeBtn(mode?.id === m.id)}>
              <span style={{ fontSize: 19 }}>{m.icon || "💳"}</span>{m.name}
            </button>
          ))}
        </div>

        {isCash && (
          <div style={{ marginTop: 14 }}>
            <div style={{ display: "flex", gap: 7, flexWrap: "wrap" }}>
              {[total, 50, 100, 200, 500].map((v, i) => (
                <button key={i} onClick={() => setTendered(i === 0 ? total : tendered + v)} style={quick}>
                  {i === 0 ? "Exact" : `+${v}`}
                </button>
              ))}
              <button onClick={() => setTendered(0)} style={{ ...quick, color: "var(--neg)" }}>Clear</button>
              <label style={{ display: "flex", alignItems: "center", gap: 6, marginInlineStart: "auto", fontSize: 12, color: "var(--ink-muted)" }}>
                <input type="checkbox" checked={showDenoms} onChange={e => setShowDenoms(e.target.checked)} /> Denominations
              </label>
            </div>
            {showDenoms && (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 7, marginTop: 9 }}>
                {denoms.map(d => (
                  <button key={d.label} onClick={() => setTendered(+(tendered + d.value).toFixed(2))} style={den(d.kind)}>
                    {d.value >= 1 ? d.value : d.label.split(" ")[0]}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        <button disabled={!mode || balance > 0}
          onClick={async () => {
            const pay = [{ payment_mode: mode?.id, amount: isCash ? tendered : total }];
            if (orderNo) {
              try {
                const r = await fetch(`${"/api/method/alphax_pos.alphax_pos.api.payment.complete"}`, {
                  method: "POST", credentials: "include",
                  headers: { "Content-Type": "application/json",
                    "X-Frappe-CSRF-Token": (window as any).csrf_token || "" },
                  body: JSON.stringify({ order_no: orderNo, payments: JSON.stringify(pay) }),
                });
                const d = await r.json();
                onPaid?.(d.message || { total, paid: pay[0].amount, change });
              } catch (e) {
                onPaid?.({ total, paid: pay[0].amount, change, offline: true });
              }
            } else {
              onPaid?.({ total, paid: pay[0].amount, change, demo: true });
            }
            onClose();
          }}
          style={confirm(!!mode && balance <= 0)}>
          {mode?.requires_terminal ? "Push to card reader" : balance > 0 ? `Balance SAR ${balance.toFixed(2)}` : "Confirm payment"}
        </button>
      </div>
    </div>
  );
}

function Cell({ label, value, big, accent, tone }: any) {
  const color = tone === "pos" ? "var(--pos)" : tone === "neg" ? "var(--ink)" : accent ? "var(--brand)" : "var(--ink)";
  return (
    <div style={{ textAlign: "center", flex: 1 }}>
      <div style={{ fontSize: 11, color: "var(--ink-muted)", marginBottom: 3 }}>{label}</div>
      <div className="num" style={{ fontSize: big ? 22 : 18, fontWeight: 800, color }}>
        <span style={{ fontSize: 11, color: "var(--ink-faint)" }}>SAR </span>{value.toFixed(2)}
      </div>
    </div>
  );
}

const FALLBACK: Mode[] = [
  { id: "cash", name: "Cash", kind: "cash", icon: "💵" },
  { id: "mada", name: "mada", kind: "card", icon: "💳", requires_terminal: 1 },
  { id: "visa", name: "Visa / MC", kind: "card", icon: "💳", requires_terminal: 1 },
  { id: "apple_pay", name: "Apple Pay", kind: "wallet", icon: "" },
  { id: "stc_pay", name: "STC Pay", kind: "wallet", icon: "📲" },
  { id: "split", name: "Split", kind: "split", icon: "🔀" },
];
const DEN: Denom[] = [
  { label: "500", value: 500, kind: "note" }, { label: "200", value: 200, kind: "note" },
  { label: "100", value: 100, kind: "note" }, { label: "50", value: 50, kind: "note" },
  { label: "10", value: 10, kind: "note" }, { label: "5", value: 5, kind: "note" },
  { label: "1", value: 1, kind: "coin" }, { label: "0.50", value: 0.5, kind: "coin" },
  { label: "0.25", value: 0.25, kind: "coin" }, { label: "0.10", value: 0.1, kind: "coin" },
];
const overlay: React.CSSProperties = { position: "fixed", inset: 0, background: "rgba(0,0,0,.45)", display: "grid", placeItems: "center", zIndex: 50 };
const sheet: React.CSSProperties = { background: "var(--surface)", borderRadius: 18, padding: 20, width: "min(520px,94vw)", boxShadow: "var(--shadow)" };
const strip: React.CSSProperties = { display: "flex", gap: 8, marginTop: 12, padding: "14px 8px", background: "var(--surface-2)", borderRadius: 14 };
function modeBtn(on: boolean): React.CSSProperties {
  return { height: 58, borderRadius: 13, display: "flex", alignItems: "center", gap: 9, padding: "0 14px",
    fontWeight: 700, fontSize: 13.5, cursor: "pointer", color: "var(--ink)",
    border: on ? "2px solid var(--brand)" : "1px solid var(--border)",
    background: on ? "var(--brand-tint)" : "var(--surface)" };
}
const quick: React.CSSProperties = { height: 38, padding: "0 13px", borderRadius: 10, fontWeight: 700, fontSize: 13,
  border: "1px solid var(--border)", background: "var(--surface)", color: "var(--ink)", cursor: "pointer" };
function den(kind: string): React.CSSProperties {
  return { height: 42, borderRadius: 10, fontWeight: 700, fontSize: 13, cursor: "pointer", color: "var(--ink)",
    border: "1px solid var(--border)", background: kind === "coin" ? "var(--surface-2)" : "var(--surface)" };
}
function confirm(active: boolean): React.CSSProperties {
  return { marginTop: 16, width: "100%", height: 60, borderRadius: 15, border: "none", fontWeight: 800, fontSize: 16,
    cursor: active ? "pointer" : "default", background: active ? "var(--brand)" : "var(--surface-3)",
    color: active ? "var(--brand-contrast)" : "var(--ink-faint)" };
}
