from __future__ import annotations

import frappe
from frappe.utils import flt, getdate, today

"""Loyalty rides ERPNext's NATIVE loyalty engine:

  • Loyalty Program       — earn/collection rules, tiers, points→currency factor
  • Loyalty Point Entry    — the points ledger (earn on Sales Invoice submit,
                             redeem when the invoice redeems points)

AlphaX adds only a thin **AlphaX Loyalty Card** master so a physical/virtual card
number (or mobile/barcode) resolves to a Customer. No parallel points ledger.
"""


@frappe.whitelist()
def lookup(query, loyalty_program=None):
    """Resolve a card by card_no, barcode or mobile → customer + live balance."""
    card = None
    for field in ("card_no", "barcode", "mobile"):
        name = frappe.db.get_value("AlphaX Loyalty Card", {field: query}, "name")
        if name:
            card = frappe.get_doc("AlphaX Loyalty Card", name)
            break
    if not card:
        return {"found": False}

    program = card.loyalty_program or loyalty_program
    bal = balance(card.customer, program) if program else {"points": 0, "value": 0}
    return {
        "found": True, "card": card.name, "status": card.status,
        "customer": card.customer,
        "customer_name": frappe.db.get_value("Customer", card.customer, "customer_name"),
        "loyalty_program": program, "tier": card.tier,
        "points": bal["points"], "value": bal["value"],
    }


def balance(customer, loyalty_program):
    """Live points balance from native Loyalty Point Entry (non-expired)."""
    rows = frappe.get_all("Loyalty Point Entry",
        filters={"customer": customer, "loyalty_program": loyalty_program},
        fields=["loyalty_points", "expiry_date"])
    pts = sum(flt(r.loyalty_points) for r in rows
              if not r.expiry_date or getdate(r.expiry_date) >= getdate(today()))
    cf = flt(frappe.db.get_value("Loyalty Program", loyalty_program, "conversion_factor"))
    return {"points": pts, "value": flt(pts) * cf}


@frappe.whitelist()
def redeem_value(points, loyalty_program):
    """Currency value of N points for this program (conversion_factor)."""
    cf = flt(frappe.db.get_value("Loyalty Program", loyalty_program, "conversion_factor"))
    return {"points": flt(points), "value": flt(points) * cf}


@frappe.whitelist()
def points_for_amount(amount, loyalty_program):
    """How many points an amount would redeem (inverse of conversion_factor)."""
    cf = flt(frappe.db.get_value("Loyalty Program", loyalty_program, "conversion_factor"))
    return {"points": (flt(amount) / cf) if cf else 0}


def sync_card_balance(card_no):
    """Refresh the cached balance/value/tier shown on the card master."""
    card = frappe.get_doc("AlphaX Loyalty Card", card_no)
    if not card.loyalty_program:
        return
    bal = balance(card.customer, card.loyalty_program)
    card.db_set("points_balance", bal["points"])
    card.db_set("points_value", bal["value"])


def apply_to_invoice(si, loyalty_program=None, redeem_points=0, redemption_account=None):
    """Attach loyalty to the Sales Invoice the POS order posts. Earning happens
    automatically on submit; redemption is handled natively when flagged.

    Call this from the SI-posting step (out of PCI/stock scope, pure accounting).
    """
    if loyalty_program:
        si.loyalty_program = loyalty_program          # native earn on submit
    if flt(redeem_points) > 0:
        si.redeem_loyalty_points = 1
        si.loyalty_points = flt(redeem_points)
        if redemption_account:
            si.loyalty_redemption_account = redemption_account
    return si
