from __future__ import annotations

app_name = "alphax_pos"
app_title = "AlphaX POS"
app_publisher = "Neotec Integrated Solution"
app_description = "Multi-vertical, white-label point of sale for ERPNext — restaurant, cafe, cafeteria, supermarket, pharmacy, retail, hotel. KSA/GCC, ZATCA-native."
app_email = "support@neotec.ai"
app_license = "mit"
app_logo_url = "/assets/alphax_pos/images/alphax-icon.svg"

add_to_apps_screen = [
    {
        "name": "alphax_pos",
        "logo": "/assets/alphax_pos/images/alphax-icon.svg",
        "title": "AlphaX POS",
        "route": "/pos",
    }
]

after_install = "alphax_pos.install.after_install"
after_migrate = ["alphax_pos.install.after_migrate"]

# Keep table status in sync; backflush stock to a Stock Issue entry on payment.
doc_events = {
    "AlphaX POS Order": {
        "on_update": "alphax_pos.alphax_pos.api.order.sync_table_status",
    },
}

scheduler_events = {
    "cron": {
        # batched recipe backflush + aggregator status mirror
        "*/5 * * * *": ["alphax_pos.tasks.poll_aggregators"],
    },
    "daily": ["alphax_pos.tasks.nightly_backflush"],
}

website_route_rules = [
    {"from_route": "/pos/<path:app_path>", "to_route": "pos"},
]

fixtures = [
    "AlphaX Theme",
    "AlphaX Payment Mode",
    "AlphaX Currency Denomination",
    {"dt": "Role", "filters": [["role_name", "in", ["AlphaX POS Manager", "AlphaX POS User"]]]},
    {"dt": "Custom Field", "filters": [["name", "=", "Stock Entry-alphax_pos_order"]]},
]
