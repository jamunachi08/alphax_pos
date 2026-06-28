from __future__ import annotations

import json
import frappe


def _aggregate(order):
    """Resolve every order line's recipe (+ modifier recipe_delta) into a
    consolidated {(raw_item, uom): qty} map. Runs entirely server-side — the
    cashier screen never sees this; it is a pure backend stock movement."""
    bucket: dict[tuple, float] = {}

    def add(raw_item, qty, uom):
        key = (raw_item, uom or "")
        bucket[key] = bucket.get(key, 0) + qty

    for line in order.lines:
        if not frappe.db.exists("AlphaX Recipe", line.menu_item):
            continue
        recipe = frappe.get_doc("AlphaX Recipe", line.menu_item)
        yield_qty = recipe.yield_qty or 1
        factor = (line.qty or 1) / yield_qty
        for rl in recipe.lines:
            add(rl.raw_item, (rl.qty or 0) * factor, rl.uom)

        # modifier deltas: JSON like {"-Milk":150,"+Oat milk":150,"uom":"ml"}
        if line.modifiers:
            try:
                mods = json.loads(line.modifiers)
            except Exception:
                mods = []
            for m in mods if isinstance(mods, list) else []:
                for raw, spec in (m.get("recipe_delta") or {}).items():
                    qty = float(spec.get("qty", 0)) * (line.qty or 1)
                    add(raw, qty, spec.get("uom"))
    return bucket


@frappe.whitelist()
def resolve(order_no):
    """Preview the consolidated consumption for an order (for reports/audit)."""
    order = frappe.get_doc("AlphaX POS Order", order_no)
    return [{"raw_item": k[0], "uom": k[1], "qty": v} for k, v in _aggregate(order).items()]


def backflush(order_no, submit=True):
    """Create (and submit) a Material Issue Stock Entry that depletes the raw
    components for an order. Idempotent: skips if already issued. Returns the
    Stock Entry name. This is invoked from payment completion, not the UI."""
    order = frappe.get_doc("AlphaX POS Order", order_no)
    if frappe.db.exists("Stock Entry", {"alphax_pos_order": order_no}):
        return frappe.db.get_value("Stock Entry", {"alphax_pos_order": order_no}, "name")

    profile = frappe.get_doc("AlphaX POS Profile", order.pos_profile)
    outlet = frappe.get_doc("AlphaX Outlet", profile.outlet)
    warehouse = outlet.warehouse
    if not warehouse:
        frappe.log_error(f"AlphaX: no warehouse for outlet {outlet.name}", "AlphaX backflush")
        return None

    consumption = _aggregate(order)
    if not consumption:
        return None

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.purpose = "Material Issue"
    se.company = outlet.company
    # custom link field added via fixtures/custom field in real install:
    se.alphax_pos_order = order_no
    for (raw_item, uom), qty in consumption.items():
        se.append("items", {
            "item_code": raw_item,
            "qty": qty,
            "uom": uom or None,
            "s_warehouse": warehouse,
        })
    se.insert(ignore_permissions=True)
    if submit:
        se.submit()
    frappe.db.commit()
    return se.name
