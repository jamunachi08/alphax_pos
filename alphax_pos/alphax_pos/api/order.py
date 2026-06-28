from __future__ import annotations

import json
import frappe
from frappe.utils import flt


@frappe.whitelist()
def create(order):
    """Persist a cart as an AlphaX POS Order and return its number + totals."""
    if isinstance(order, str):
        order = json.loads(order)

    lines = order.get("lines") or []
    if not lines:
        frappe.throw("Cannot create an empty order")

    doc = frappe.new_doc("AlphaX POS Order")
    doc.pos_profile = order.get("pos_profile")
    doc.terminal = order.get("terminal")
    doc.order_type = order.get("order_type") or "dine_in"
    doc.table = order.get("table")
    doc.customer = order.get("customer")
    doc.status = "open"

    subtotal = 0.0
    for ln in lines:
        qty = flt(ln.get("qty") or 1)
        rate = flt(ln.get("rate") or 0)
        amount = qty * rate
        subtotal += amount
        doc.append("lines", {
            "menu_item": ln.get("menu_item"),
            "item_label": ln.get("item_label"),
            "qty": qty, "rate": rate, "amount": amount,
            "modifiers": ln.get("modifiers"),
        })

    discount = flt(order.get("discount") or 0)
    vat_rate = flt(order.get("vat_rate") if order.get("vat_rate") is not None else 15)
    taxable = max(0.0, subtotal - discount)
    vat = taxable * vat_rate / 100.0

    doc.subtotal = subtotal
    doc.discount = discount
    doc.vat = vat
    doc.total = taxable + vat
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"order_no": doc.name, "subtotal": subtotal, "discount": discount,
            "vat": vat, "total": doc.total}


@frappe.whitelist()
def fire_kot(order_no):
    """Split order lines by category.kitchen_station → one KOT per station."""
    pass


@frappe.whitelist()
def hold(order_no):
    frappe.db.set_value("AlphaX POS Order", order_no, "status", "open")
    frappe.db.set_value("AlphaX POS Order", order_no, "channel", "held")
    return {"held": order_no}


@frappe.whitelist()
def release(order_no=None, terminal=None):
    """Recall a held order (by name, or the latest held one on this terminal)."""
    if not order_no:
        order_no = frappe.db.get_value("AlphaX POS Order",
            {"channel": "held", "terminal": terminal}, "name", order_by="modified desc")
    if not order_no:
        return {"released": None}
    frappe.db.set_value("AlphaX POS Order", order_no, "channel", "pos")
    return {"released": order_no}


@frappe.whitelist()
def sales_return(original_order, lines=None):
    """Create a return order referencing an original sale (full or line-level)."""
    src = frappe.get_doc("AlphaX POS Order", original_order)
    ret = frappe.copy_doc(src)
    ret.status = "open"
    ret.channel = "return"
    ret.aggregator_ref = f"RETURN OF {original_order}"
    for ln in ret.lines:
        ln.qty = -abs(ln.qty or 0)
    ret.insert(ignore_permissions=True)
    return {"return_order": ret.name}


@frappe.whitelist()
def reprint_last(terminal):
    """Return the most recent paid invoice for this terminal to reprint."""
    name = frappe.db.get_value("AlphaX POS Order",
        {"terminal": terminal, "status": "paid"}, "name", order_by="modified desc")
    return {"order": name}


def sync_table_status(doc, method=None):
    if not doc.table:
        return
    status = "free" if doc.status in ("paid", "void") else "seated"
    frappe.db.set_value("AlphaX Table", doc.table, "status", status)
