from __future__ import annotations

import frappe
import frappe.sessions

no_cache = 1


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/pos"
        raise frappe.Redirect
    csrf_token = frappe.sessions.get_csrf_token()
    frappe.db.commit()  # nosemgrep — required for SPA bootstrapping
    context.csrf_token = csrf_token
    context.frappe_user = frappe.session.user
    context.no_cache = 1
    context.show_sidebar = False
    return context
