from __future__ import annotations

import json
import frappe


@frappe.whitelist()
def get_boot():
    """Single call the SPA makes on load: branding + resolved theme + payment modes.

    This is what makes the product feel like the customer\'s own: every label,
    colour, logo and currency comes from AlphaX Branding + the active theme.
    """
    b = frappe.get_single("AlphaX Branding")
    theme = _resolve_theme(b.primary_theme or "majlis-green")
    return {
        "branding": {
            "brand_name": b.brand_name or "AlphaX POS",
            "legal_name": b.legal_name,
            "tagline": b.tagline,
            "tagline_ar": b.tagline_ar,
            "logo_light": b.logo_light,
            "logo_dark": b.logo_dark,
            "app_icon": b.app_icon,
            "favicon": b.favicon,
            "allow_theme_switch": bool(b.allow_theme_switch),
            "allow_theme_custom": bool(b.allow_theme_custom),
            "force_mode": b.force_mode or "Auto",
            "show_powered_by": bool(b.show_powered_by),
            "support_email": b.support_email,
            "support_phone": b.support_phone,
            "website": b.website,
            "default_language": b.default_language or "en",
            "enable_arabic": bool(b.enable_arabic),
            "currency_symbol": b.currency_symbol or "SAR",
            "receipt_header": b.receipt_header,
            "receipt_footer": b.receipt_footer,
        },
        "theme": theme,
        "themes": list_themes(),
        "session": _session(),
    }


def _session():
    """Best-effort terminal/profile/outlet context for the running cashier.

    Returns None when nothing is configured yet — the SPA then renders a demo
    catalog so the screen is never blank during setup.
    """
    try:
        user = frappe.session.user
        shift = frappe.db.get_value("AlphaX Shift",
            {"cashier": user, "status": "open"}, ["name", "terminal"], as_dict=True)
        terminal = shift.terminal if shift else frappe.db.get_value("AlphaX Terminal", {}, "name")
        if not terminal:
            return None
        t = frappe.db.get_value("AlphaX Terminal", terminal,
            ["name", "pos_profile", "default_floor"], as_dict=True)
        prof = None
        if t and t.pos_profile:
            prof = frappe.db.get_value("AlphaX POS Profile", t.pos_profile,
                ["name", "outlet", "vat_rate", "vertical", "default_customer",
                 "enable_tables", "enable_kot", "enable_modifiers", "enable_delivery",
                 "enable_loyalty"], as_dict=True)
        outlet = None
        if prof and prof.outlet:
            outlet = frappe.db.get_value("AlphaX Outlet", prof.outlet,
                ["outlet_name", "outlet_name_ar", "vertical"], as_dict=True)
        return {
            "terminal": terminal,
            "pos_profile": prof.name if prof else None,
            "default_floor": t.default_floor if t else None,
            "vat_rate": float(prof.vat_rate) if (prof and prof.vat_rate) else 15.0,
            "vertical": (prof.vertical if prof else None) or (outlet.vertical if outlet else "cafe"),
            "outlet_name": outlet.outlet_name if outlet else None,
            "outlet_name_ar": outlet.outlet_name_ar if outlet else None,
            "default_customer": prof.default_customer if prof else None,
            "cashier": frappe.db.get_value("User", user, "full_name") or user,
            "shift": shift.name if shift else None,
            "features": {
                "tables": bool(prof.enable_tables) if prof else False,
                "kot": bool(prof.enable_kot) if prof else False,
                "modifiers": bool(prof.enable_modifiers) if prof else False,
                "delivery": bool(prof.enable_delivery) if prof else False,
                "loyalty": bool(prof.enable_loyalty) if prof else False,
            },
        }
    except Exception:
        frappe.log_error(frappe.get_traceback(), "AlphaX POS boot session")
        return None


def _resolve_theme(theme_id):
    if not frappe.db.exists("AlphaX Theme", theme_id):
        theme_id = "majlis-green"
    t = frappe.get_doc("AlphaX Theme", theme_id)
    try:
        tokens = json.loads(t.tokens_json) if t.tokens_json else {}
    except Exception:
        tokens = {}
    return {"id": t.theme_id, "name": t.theme_name, "name_ar": t.theme_name_ar,
            "base": t.base, "tokens": tokens}


@frappe.whitelist()
def list_themes():
    rows = frappe.get_all("AlphaX Theme",
        fields=["theme_id", "theme_name", "theme_name_ar", "base", "vertical_tag",
                "brand", "brand_deep", "accent", "accent_deep", "is_preset"],
        order_by="is_preset desc, theme_name asc")
    return rows


@frappe.whitelist()
def set_active_theme(theme_id):
    b = frappe.get_single("AlphaX Branding")
    b.primary_theme = theme_id
    b.save()
    frappe.db.commit()
    return _resolve_theme(theme_id)


@frappe.whitelist()
def save_custom_theme(theme_name, brand, accent, base="warm",
                      brand_deep=None, accent_deep=None, make_active=0):
    """Custom theme provision: persist a customer's own colours as a reusable
    AlphaX Theme (is_preset=0). Builds the FULL token set with the same engine
    the seeded presets use, so the saved theme carries its complete palette and
    can be selected from Branding or the terminal picker, re-edited, or deleted.
    Only brand + accent are required; deep shades are derived if omitted.
    """
    from alphax_pos.install import _tokens

    brand_deep = brand_deep or _darken(brand)
    accent_deep = accent_deep or _darken(accent)
    tokens = _tokens(base, brand, brand_deep, accent, accent_deep)

    theme_id = "custom-" + frappe.scrub(theme_name).replace("_", "-")
    data = {"theme_name": theme_name, "base": base, "is_preset": 0,
            "vertical_tag": "custom", "brand": brand, "brand_deep": brand_deep,
            "accent": accent, "accent_deep": accent_deep,
            "tokens_json": json.dumps(tokens)}

    if frappe.db.exists("AlphaX Theme", theme_id):
        doc = frappe.get_doc("AlphaX Theme", theme_id)
        doc.update(data)
        doc.save(ignore_permissions=True)
    else:
        d = {"doctype": "AlphaX Theme", "theme_id": theme_id}
        d.update(data)
        frappe.get_doc(d).insert(ignore_permissions=True)

    if int(make_active or 0):
        b = frappe.get_single("AlphaX Branding")
        b.primary_theme = theme_id
        b.save(ignore_permissions=True)
    frappe.db.commit()
    return _resolve_theme(theme_id)


@frappe.whitelist()
def delete_custom_theme(theme_id):
    doc = frappe.get_doc("AlphaX Theme", theme_id)
    if doc.is_preset:
        frappe.throw("Preset themes cannot be deleted.")
    frappe.delete_doc("AlphaX Theme", theme_id)
    frappe.db.commit()
    return {"deleted": theme_id}


def _darken(hexc, amt=0.22):
    hexc = (hexc or "#000000").lstrip("#")
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    f = 1 - amt
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))
