from __future__ import annotations
import frappe

@frappe.whitelist()
def tree(pos_profile=None):
    cats = frappe.get_all("AlphaX Menu Category",
        fields=["name","category_name","category_name_ar","color","icon","kitchen_station","sort"],
        order_by="sort asc")
    items = frappe.get_all("AlphaX Menu Item",
        fields=["name","item_label","item_label_ar","category","price","emoji","image","is_86","has_modifiers"])
    return {"categories": cats, "items": items}
