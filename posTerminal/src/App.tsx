import { useBoot } from "./theme/useBoot";
import POSScreen from "./features/pos/POSScreen";

export default function App() {
  const boot = useBoot();
  if (!boot) {
    return (
      <div style={{ display: "grid", placeItems: "center", height: "100%", color: "var(--ink-muted)" }}>
        Loading…
      </div>
    );
  }
  return <POSScreen boot={boot} />;
}
