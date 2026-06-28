from __future__ import annotations
import frappe

@frappe.whitelist()
def vertical_config(vertical):
    """Feature flags a surface should honour for a given vertical."""
    base = dict(tables=False, kot=False, modifiers=False, recipe=False,
                barcode=False, weight=False, batch_expiry=False, room_charge=False)
    presets = {
        "restaurant": dict(tables=True, kot=True, modifiers=True, recipe=True),
        "cafe":       dict(tables=True, kot=True, modifiers=True, recipe=True),
        "cafeteria":  dict(kot=True, recipe=True),
        "supermarket":dict(barcode=True, weight=True),
        "pharmacy":   dict(barcode=True, batch_expiry=True),
        "retail":     dict(barcode=True),
        "hotel":      dict(tables=True, kot=True, modifiers=True, recipe=True, room_charge=True),
    }
    base.update(presets.get(vertical, {}))
    return base
