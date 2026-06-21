# AlphaX POS

Multi-vertical, white-label point of sale for ERPNext / Frappe v15 — built the Neotec Insight way
(React 19 + TS + Vite SPA, whitelisted `api/` methods, design-token theming, EN/AR, ZATCA-native).

**One codebase fits:** restaurant · cafe · cafeteria · supermarket · pharmacy · retail · hotel.

## White-label in one document
Everything that makes the product feel like the customer's own lives in a single **AlphaX Branding**
doc (Setup → AlphaX Branding): brand name, logos, favicon, login screen, receipt header/footer,
currency, language, and the default **theme**. The SPA fetches it via `api.boot.get_boot` on load.

## Themes
A library of ready-made colour themes is seeded on install (`AlphaX Theme`). Pick one in Branding,
or let staff switch on the terminal (`allow_theme_switch`), or tweak brand/accent colours live
(`allow_theme_custom`). Each theme is just a set of CSS variables, so the whole UI re-skins instantly.
Add your own theme by creating a new `AlphaX Theme` record.

## Verticals
`AlphaX Outlet.vertical` / `AlphaX POS Profile.vertical` drive feature flags
(`api.setup.vertical_config`): tables/KOT/modifiers/recipe for food service; barcode/weight for
supermarket; batch/expiry for pharmacy; room charge for hotel.

## Payment modes
`AlphaX Payment Mode` masters (cash, mada, Visa/MC, Apple Pay, STC Pay, loyalty, gift card,
bank transfer, room charge, meal credit). Enable per profile via the POS Profile child table.
Card modes route to the mada terminal over ECR (`api.payment.push_to_terminal`) and capture
the result envelope (masked PAN, scheme, RRN, auth) — no raw PAN stored, staying out of PCI scope.

## Stock issue (silent backend)
Recipe depletion is **not** shown on the POS screen. When an order is paid, a single
**Material Issue Stock Entry** is generated in the background (`api.recipe.backflush`,
fired from the `AlphaX POS Order` doc event), aggregating every line's recipe plus
modifier deltas. The cashier sees nothing; stock just moves. Idempotent via `stock_issued`.
Realtime vs. scheduled is set on `POS Profile.backflush_mode`.

## Till operations (global standard)
- **Hold / Release** — park an order and recall it (`api.order.hold` / `list_held` / `release`).
- **Sales Return** — refund against a prior sale (`api.order.sales_return`, negative lines).
- **Reprint last invoice** — `api.order.reprint_last`.
- **Void**, **Discount**, attach **Customer**.
- **Cash drawer & session** (`api.shift`): Cash In, Cash Out, No Sale, X Report,
  **Shift Close**, **Day Close** with expected-vs-counted variance — backed by
  `AlphaX Cash Session` + `AlphaX Cash Movement`.

## Payment screen
`PaymentModal` shows **Total bill**, **Customer paid** (tendered) and **Change due / balance**,
supports split tender across modes, and offers an **optional denominations** pad
(`api.payment.denominations`, seeded `AlphaX Currency Denomination` for SAR) to speed cash
counting. Finalize via `api.payment.finalize`.

## Custom theme provision
Beyond the 22 presets, staff can tweak brand/accent live and **save a custom theme**
(`api.boot.save_custom_theme`) — it becomes a normal `AlphaX Theme` record (is_preset = 0),
selectable like any other. Tints derive automatically, so only four colours are needed.

## Install
```bash
bench get-app alphax_pos /path/to/alphax_pos
bench --site <site> install-app alphax_pos
# frontend
cd alphax_pos/posTerminal && npm install && npm run build
bench --site <site> clear-cache
```
Open `/pos`.

## Layout
- `alphax_pos/alphax_pos/doctype/` — data model
- `alphax_pos/alphax_pos/api/` — whitelisted endpoints (`boot`, `order`, `menu`, `payment`, `recipe`, `setup`)
- `alphax_pos/alphax_pos/install.py` — seeds themes, payment modes, roles, branding
- `posTerminal/` — Vite/React/TS SPA (theme engine in `src/theme/`)

## What AlphaX reuses from native ERPNext (vs. its own docs)

AlphaX is a **layer on top of ERPNext**, not a replacement. It reuses native masters and
posting documents wherever accounting/stock correctness depends on them:

| Concern | Native ERPNext doc used |
|---|---|
| Products / pricing | **Item**, **Item Price**, **Price List**, **UOM** |
| Parties | **Customer**, **Company** |
| Stock | **Warehouse**, **Stock Entry** (recipe backflush → Material Issue) |
| Tax / VAT (KSA 15%) | **Sales Taxes and Charges Template** (linked on the POS Profile) |
| Money / GL | **Mode of Payment** (each AlphaX Payment Mode links to one) |
| Invoicing / ZATCA | **Sales Invoice** (the order posts one; ZATCA QR rides it) |
| Loyalty | **Loyalty Program** + **Loyalty Point Entry** (native earn/redeem ledger) |

**AlphaX-specific docs exist only for the POS *experience*** that native ERPNext doesn't model:
`AlphaX POS Profile` (vertical, tables/KOT/modifiers/recipe/loyalty toggles, theme) and
`AlphaX Payment Mode` (icon, ECR routing, drawer behaviour). Both bridge to the native docs:

- `AlphaX Payment Mode.mode_of_payment` → native **Mode of Payment** (so tenders hit the right GL account).
- `AlphaX POS Profile.erpnext_pos_profile` → native **POS Profile** (income/write-off accounts, cost center).
- `AlphaX POS Profile.vat_template` → native **Sales Taxes and Charges Template**.
- `AlphaX POS Profile.loyalty_program` → native **Loyalty Program**.

This keeps the cashier experience rich while every financial figure lands in standard ERPNext
ledgers your accountants already reconcile.

## Loyalty

`AlphaX Loyalty Card` is a thin master: a card number / mobile / barcode that resolves to a
**Customer**. All points logic uses the **native** engine:

- **Earning** happens automatically when the order's **Sales Invoice** is submitted with a
  `loyalty_program` set — ERPNext writes the **Loyalty Point Entry**.
- **Redeeming** uses native invoice redemption (`redeem_loyalty_points`, `loyalty_points`,
  `loyalty_redemption_account`) — points convert to currency via the program's `conversion_factor`.
- `api/loyalty.py` provides `lookup()` (card → customer + live balance), `balance()`,
  `redeem_value()`, `points_for_amount()`, and `apply_to_invoice()` for the SI-posting step.

On the terminal, the **Loyalty** tender mode looks up the card, shows the live points balance and
its cash value, and lets the cashier redeem to cover the bill (or redeem all, with any remainder
paid by another tender).
