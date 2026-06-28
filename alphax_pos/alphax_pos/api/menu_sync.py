from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt

# Only managers (or Administrator via `bench execute`) may seed the menu.
MANAGER_ROLES = ("System Manager", "AlphaX POS Manager")


@frappe.whitelist()
def sync_from_erpnext(
    price_list,
    item_group=None,
    include_descendants=1,
    refresh_prices=0,
    create_categories=1,
    only_sales_items=1,
    limit=0,
    dry_run=0,
):
    """Seed AlphaX Menu Items from ERPNext Items, then let staff curate.

    Idempotent: each menu line is keyed on its ERPNext ``item`` link, so re-runs
    never duplicate. Existing (curated) lines are preserved — only price is
    touched, and only when ``refresh_prices`` is set. Item Group -> AlphaX Menu
    Category mapping is get-or-create.

    Args:
        price_list:         REQUIRED. Your POS selling Price List; prices come
                            from Item Price rows on this list (newest wins).
        item_group:         Limit to this Item Group. None = all groups.
        include_descendants: 1 = include child groups (nested-set lft/rgt).
        refresh_prices:     1 = update price on items that already exist.
        create_categories:  1 = create a Menu Category for each Item Group.
        only_sales_items:   1 = only Items with is_sales_item.
        limit:              cap number of Items processed (0 = no cap).
        dry_run:            1 = compute and report counts, write nothing.

    Returns: a summary dict (counts + any items missing a price on the list).
    Run from the console:
        bench --site <site> execute \\
          alphax_pos.alphax_pos.api.menu_sync.sync_from_erpnext \\
          --kwargs "{'price_list':'POS Selling','item_group':'Beverages','dry_run':1}"
    """
    frappe.only_for(MANAGER_ROLES)

    include_descendants = int(include_descendants or 0)
    refresh_prices = int(refresh_prices or 0)
    create_categories = int(create_categories or 0)
    only_sales_items = int(only_sales_items or 0)
    dry_run = int(dry_run or 0)
    limit = int(limit or 0)

    if not price_list:
        frappe.throw(_("price_list is required (your POS selling Price List)."))
    if not frappe.db.exists("Price List", price_list):
        frappe.throw(_("Price List {0} not found.").format(price_list))

    groups = _target_groups(item_group, include_descendants)

    item_filters = {"disabled": 0, "has_variants": 0}
    if only_sales_items:
        item_filters["is_sales_item"] = 1
    if groups is not None:
        item_filters["item_group"] = ["in", groups]

    items = frappe.get_all(
        "Item",
        filters=item_filters,
        fields=["name", "item_name", "item_group", "image", "stock_uom"],
        order_by="item_group asc, item_name asc",
        limit=limit or None,
    )

    price_map = _price_map(price_list, [i.name for i in items])

    cat_cache: dict[str, str] = {}
    sort_seed = _max_category_sort()
    summary = {
        "price_list": price_list,
        "groups": groups if groups is not None else "ALL",
        "items_seen": len(items),
        "categories_created": 0,
        "items_created": 0,
        "items_price_updated": 0,
        "items_skipped_existing": 0,
        "missing_price": [],
        "dry_run": bool(dry_run),
    }

    for it in items:
        # --- category get-or-create (name == category_name == Item Group) -----
        cat = cat_cache.get(it.item_group)
        if cat is None:
            cat = frappe.db.get_value(
                "AlphaX Menu Category", {"category_name": it.item_group}, "name"
            )
            if not cat and create_categories:
                sort_seed += 1
                if not dry_run:
                    doc = frappe.get_doc(
                        {
                            "doctype": "AlphaX Menu Category",
                            "category_name": it.item_group,
                            "available": 1,
                            "sort": sort_seed,
                        }
                    ).insert(ignore_permissions=True)
                    cat = doc.name
                else:
                    cat = it.item_group  # provisional name for dry-run
                summary["categories_created"] += 1
            cat_cache[it.item_group] = cat or ""

        price = price_map.get(it.name)
        if price is None:
            summary["missing_price"].append(it.name)

        # --- idempotency: one menu line per ERPNext item ----------------------
        existing = frappe.db.get_value("AlphaX Menu Item", {"item": it.name}, "name")
        if existing:
            if refresh_prices and price is not None:
                if not dry_run:
                    frappe.db.set_value("AlphaX Menu Item", existing, "price", flt(price))
                summary["items_price_updated"] += 1
            else:
                summary["items_skipped_existing"] += 1
            continue

        if not cat:
            # category absent and create_categories=0 -> skip rather than error
            summary["items_skipped_existing"] += 1
            continue

        summary["items_created"] += 1
        if not dry_run:
            frappe.get_doc(
                {
                    "doctype": "AlphaX Menu Item",
                    "item_label": _unique_label(it.item_name or it.name),
                    "category": cat,
                    "item": it.name,
                    "price": flt(price or 0),
                    "image": it.image,
                    "is_86": 0,
                }
            ).insert(ignore_permissions=True)

    if not dry_run:
        frappe.db.commit()

    if len(summary["missing_price"]) > 50:
        n = len(summary["missing_price"])
        summary["missing_price"] = summary["missing_price"][:50] + [f"... +{n - 50} more"]
    return summary


@frappe.whitelist()
def preview(price_list, item_group=None, include_descendants=1, only_sales_items=1):
    """Dry-run convenience wrapper — counts only, writes nothing."""
    return sync_from_erpnext(
        price_list=price_list,
        item_group=item_group,
        include_descendants=include_descendants,
        only_sales_items=only_sales_items,
        dry_run=1,
    )


@frappe.whitelist()
def candidate_groups():
    """Item Groups that actually contain sellable Items — for a setup picker."""
    frappe.only_for(MANAGER_ROLES)
    rows = frappe.db.sql(
        """
        select item_group as name, count(*) as items
        from `tabItem`
        where disabled = 0 and has_variants = 0 and is_sales_item = 1
        group by item_group order by items desc
        """,
        as_dict=True,
    )
    return rows


@frappe.whitelist()
def selling_price_lists():
    """Selling Price Lists — for a setup picker."""
    frappe.only_for(MANAGER_ROLES)
    return frappe.get_all(
        "Price List", filters={"selling": 1, "enabled": 1}, pluck="name"
    )


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _target_groups(item_group, include_descendants):
    if not item_group:
        return None  # all groups
    if not frappe.db.exists("Item Group", item_group):
        frappe.throw(_("Item Group {0} not found.").format(item_group))
    if not include_descendants:
        return [item_group]
    lft, rgt = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"])
    rows = frappe.get_all(
        "Item Group", filters={"lft": [">=", lft], "rgt": ["<=", rgt]}, pluck="name"
    )
    return rows or [item_group]


def _price_map(price_list, item_codes):
    """item_code -> rate from the named Price List. Newest valid_from wins."""
    if not item_codes:
        return {}
    rows = frappe.get_all(
        "Item Price",
        filters={"price_list": price_list, "item_code": ["in", item_codes]},
        fields=["item_code", "price_list_rate", "valid_from"],
        order_by="valid_from asc",  # later rows overwrite earlier -> newest wins
    )
    out: dict[str, float] = {}
    for r in rows:
        out[r.item_code] = flt(r.price_list_rate)
    return out


def _max_category_sort():
    v = frappe.db.sql("select max(sort) from `tabAlphaX Menu Category`")
    return int((v and v[0] and v[0][0]) or 0)


def _unique_label(base):
    """AlphaX Menu Item autonames on item_label, so labels must be unique."""
    label = base
    i = 2
    while frappe.db.exists("AlphaX Menu Item", label):
        label = f"{base} ({i})"
        i += 1
    return label
