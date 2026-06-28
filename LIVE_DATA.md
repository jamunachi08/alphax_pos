# Getting live data in the POS

The catalog reads from two app DocTypes — **AlphaX Menu Category** (sidebar) and
**AlphaX Menu Item** (cards). The `DEMO` badge shows only when **AlphaX Menu Item
is empty**, so the screen substitutes a demo catalog. Create one real menu item
and the badge disappears.

Each AlphaX Menu Item links an ERPNext **Item** (the `item` field) — that link is
the bridge to your stock/invoicing. You curate a touchscreen menu rather than
dumping the whole item master onto the till.

## Seed the menu from ERPNext, then curate

`api/menu_sync.py` builds menu items from your ERPNext Items, idempotently
(keyed on the ERPNext `item` link — re-runs never duplicate). Prices come from a
**specific selling Price List** you name (newest `Item Price` wins). Item Group →
Menu Category mapping is get-or-create.

### 1. Dry-run first (writes nothing, just counts)
```bash
bench --site <site> execute \
  alphax_pos.alphax_pos.api.menu_sync.preview \
  --kwargs "{'price_list':'POS Selling','item_group':'Beverages'}"
```
Returns `items_seen`, `items_created`, `categories_created`, and any
`missing_price` (Items with no rate on that list).

### 2. Run it
```bash
bench --site <site> execute \
  alphax_pos.alphax_pos.api.menu_sync.sync_from_erpnext \
  --kwargs "{'price_list':'POS Selling','item_group':'Beverages','include_descendants':1}"
```
Open `/pos` → DEMO gone, live items render.

### 3. Re-run any time
- New Items added in ERPNext → re-run; only the new ones are created.
- Changed prices → add `'refresh_prices':1` to update prices on existing lines
  while leaving your curated labels/emoji/flags untouched.

### Parameters
| arg | default | meaning |
|---|---|---|
| `price_list` | — (required) | selling Price List to read rates from |
| `item_group` | None | limit to one group; None = all groups |
| `include_descendants` | 1 | include child Item Groups |
| `refresh_prices` | 0 | update price on already-existing menu items |
| `create_categories` | 1 | create a Menu Category per Item Group |
| `only_sales_items` | 1 | only Items flagged `is_sales_item` |
| `limit` | 0 | cap Items processed (0 = no cap) |
| `dry_run` | 0 | report counts, write nothing |

Helpers for a future setup screen: `candidate_groups()` (groups with sellable
items + counts) and `selling_price_lists()`. All methods are whitelisted and
restricted to **System Manager / AlphaX POS Manager**.

## After seeding — curate
Open **AlphaX Menu Item** list: set Arabic labels (`item_label_ar`), emoji/image,
`is_86` (sold out), `has_modifiers`, kitchen station on the category, and `sort`
order. The sync won't overwrite these on re-run.
