export type Vertical =
  | "restaurant" | "cafe" | "cafeteria" | "supermarket" | "pharmacy" | "retail" | "hotel";

export interface VerticalConfig {
  tables: boolean; kot: boolean; modifiers: boolean; recipe: boolean;
  barcode: boolean; weight: boolean; batchExpiry: boolean; roomCharge: boolean;
  layout: "menu-grid" | "scan-list";
}

const base: VerticalConfig = {
  tables: false, kot: false, modifiers: false, recipe: false,
  barcode: false, weight: false, batchExpiry: false, roomCharge: false, layout: "menu-grid",
};

export const VERTICALS: Record<Vertical, VerticalConfig> = {
  restaurant:  { ...base, tables: true, kot: true, modifiers: true, recipe: true },
  cafe:        { ...base, tables: true, kot: true, modifiers: true, recipe: true },
  cafeteria:   { ...base, kot: true, recipe: true },
  supermarket: { ...base, barcode: true, weight: true, layout: "scan-list" },
  pharmacy:    { ...base, barcode: true, batchExpiry: true, layout: "scan-list" },
  retail:      { ...base, barcode: true, layout: "scan-list" },
  hotel:       { ...base, tables: true, kot: true, modifiers: true, recipe: true, roomCharge: true },
};
