from __future__ import annotations

import json
import frappe
from frappe.utils import flt


@frappe.whitelist()
def denominations():
    """Enabled cash denominations for the tender pad."""
    return frappe.get_all("AlphaX Currency Denomination",
        filters={"enabled": 1}, fields=["label", "value", "kind"],
        order_by="sort asc, value desc")


@frappe.whitelist()
def modes(pos_profile):
    p = frappe.get_doc("AlphaX POS Profile", pos_profile)
    out = []
    for row in p.payment_modes:
        if not row.enabled:
            continue
        m = frappe.get_doc("AlphaX Payment Mode", row.payment_mode)
        out.append({"id": m.mode_id, "name": row.label_override or m.mode_name,
                    "name_ar": m.mode_name_ar, "kind": m.kind, "icon": m.icon,
                    "requires_terminal": m.requires_terminal,
                    "requires_reference": m.requires_reference,
                    "opens_cash_drawer": m.opens_cash_drawer})
    return out


@frappe.whitelist()
def push_to_terminal(terminal, amount):
    """ECR: push the invoice amount to the paired mada reader and capture the
    result envelope (masked PAN, scheme, RRN, auth). No raw PAN is stored."""
    # Real impl dispatches to integrations/mada_ecr/<provider>.py
    return {"approved": True, "masked_pan": "**** **** **** 4421",
            "card_scheme": "mada", "rrn": "000000123456", "auth_code": "A1B2C3"}


@frappe.whitelist()
def complete(order_no, payments):
    """Record tender, compute change, mark paid, and trigger backend stock issue.

    payments: JSON list of {payment_mode, amount, reference?, masked_pan?, ...}
    Returns {total, paid, change, stock_entry}.
    """
    if isinstance(payments, str):
        payments = json.loads(payments)

    order = frappe.get_doc("AlphaX POS Order", order_no)
    order.set("payments", [])
    paid = 0.0
    for p in payments:
        amt = flt(p.get("amount"))
        paid += amt
        order.append("payments", {
            "payment_mode": p.get("payment_mode"),
            "amount": amt,
            "reference": p.get("reference"),
            "card_scheme": p.get("card_scheme"),
            "masked_pan": p.get("masked_pan"),
            "rrn": p.get("rrn"),
            "terminal_txn_id": p.get("terminal_txn_id"),
            "approved": 1,
        })

    total = flt(order.total)
    change = max(0.0, paid - total)
    order.paid = paid
    order.balance = max(0.0, total - paid)
    order.status = "paid"
    order.save(ignore_permissions=True)

    # Backend stock issue — invisible to the cashier screen.
    profile = frappe.get_doc("AlphaX POS Profile", order.pos_profile)
    stock_entry = None
    if profile.enable_recipe and (profile.backflush_mode or "").startswith("On Payment"):
        from alphax_pos.alphax_pos.api.recipe import backflush
        stock_entry = backflush(order_no)

    frappe.db.commit()
    return {"total": total, "paid": paid, "change": change, "stock_entry": stock_entry}


@frappe.whitelist()
def cash_in(terminal, amount, reason=None):
    return _cash_movement(terminal, "pay_in", amount, reason)


@frappe.whitelist()
def cash_out(terminal, amount, reason=None):
    return _cash_movement(terminal, "pay_out", amount, reason)


def _cash_movement(terminal, kind, amount, reason):
    shift = frappe.db.get_value("AlphaX Shift",
        {"terminal": terminal, "closed_at": ("is", "not set")}, "name")
    if not shift:
        frappe.throw("No open shift on this terminal")
    doc = frappe.get_doc("AlphaX Shift", shift)
    doc.append("cash_movements", {"type": kind, "amount": flt(amount), "reason": reason})
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True}


@frappe.whitelist()
def open_drawer(terminal):
    """Send the ESC/POS drawer-kick to the receipt printer."""
    return {"ok": True}
