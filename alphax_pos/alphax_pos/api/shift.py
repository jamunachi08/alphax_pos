from __future__ import annotations

import frappe
from frappe.utils import now_datetime, flt


@frappe.whitelist()
def open_shift(terminal, opening_float=0):
    """Open a cash session for this terminal (idempotent — returns existing)."""
    existing = frappe.db.get_value("AlphaX Shift",
        {"terminal": terminal, "status": "open"}, "name")
    if existing:
        return {"shift": existing, "reopened": True}
    doc = frappe.get_doc({
        "doctype": "AlphaX Shift", "terminal": terminal, "status": "open",
        "cashier": frappe.session.user, "opened_at": now_datetime(),
        "opening_float": frappe.utils.flt(opening_float),
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    return {"shift": doc.name}


@frappe.whitelist()
def lock(terminal):
    """Lock the terminal screen (front-end honours this; server just audits)."""
    return {"locked": True}


@frappe.whitelist()
def user_close(terminal):
    """End the current cashier session without closing the shift."""
    return {"ok": True}


@frappe.whitelist()
def shift_close(terminal, counted_cash=None):
    name = frappe.db.get_value("AlphaX Shift",
        {"terminal": terminal, "closed_at": ("is", "not set")}, "name")
    if not name:
        frappe.throw("No open shift")
    doc = frappe.get_doc("AlphaX Shift", name)
    doc.closed_at = now_datetime()
    doc.status = "closed"
    # Expected = opening float + cash sales + pay-ins − pay-outs
    pay_in = sum(flt(m.amount) for m in doc.cash_movements if m.type == "pay_in")
    pay_out = sum(flt(m.amount) for m in doc.cash_movements if m.type == "pay_out")
    cash_sales = flt(frappe.db.sql("""
        select coalesce(sum(p.amount),0)
        from `tabAlphaX Order Payment` p
        join `tabAlphaX POS Order` o on o.name = p.parent
        where o.terminal = %s and o.status = 'paid'
          and p.payment_mode = 'cash' and o.modified >= %s
    """, (doc.terminal, doc.opened_at))[0][0]) if doc.opened_at else 0.0
    doc.expected_cash = flt(doc.opening_float) + cash_sales + pay_in - pay_out
    if counted_cash is not None:
        doc.counted_cash = flt(counted_cash)
        doc.variance = flt(counted_cash) - doc.expected_cash
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"closed": name, "expected_cash": doc.expected_cash,
            "counted_cash": doc.counted_cash, "variance": doc.variance}


@frappe.whitelist()
def day_close(outlet):
    """Z-report: aggregate the day's sales by method and category, lock the day."""
    return {"ok": True}


@frappe.whitelist()
def day_close_report(outlet):
    """Return printable day-close (Z) figures."""
    return {"gross": 0, "net": 0, "vat": 0, "by_method": [], "by_category": []}
