from __future__ import annotations

import frappe
from frappe import _

# Logical canvas the editor and any consumer (POS) both render against.
# Table x/y are stored as pixel coordinates within this stage.
STAGE_W = 900
STAGE_H = 520


@frappe.whitelist()
def save_position(table: str, x, y) -> dict:
    """Persist a single table's position after a drag in the floor designer."""
    if not frappe.has_permission("AlphaX Table", "write", doc=table):
        frappe.throw(_("Not permitted to move this table"), frappe.PermissionError)

    nx = max(0, min(int(float(x)), STAGE_W))
    ny = max(0, min(int(float(y)), STAGE_H))
    frappe.db.set_value("AlphaX Table", table, {"x": nx, "y": ny})
    return {"table": table, "x": nx, "y": ny}


@frappe.whitelist()
def get_plan(floor: str) -> dict:
    """Floor image + its tables — used by the designer and the POS floor view."""
    fl = frappe.db.get_value(
        "AlphaX Floor",
        floor,
        ["name", "floor_name", "floor_image"],
        as_dict=True,
    )
    if not fl:
        frappe.throw(_("Floor {0} not found").format(floor))

    tables = frappe.get_all(
        "AlphaX Table",
        filters={"floor": floor},
        fields=[
            "name", "table_label", "x", "y", "shape",
            "status", "seats", "table_image", "current_order",
        ],
        order_by="table_label asc",
    )
    return {"floor": fl, "stage": {"w": STAGE_W, "h": STAGE_H}, "tables": tables}
