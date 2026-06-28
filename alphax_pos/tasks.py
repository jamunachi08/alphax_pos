from __future__ import annotations

import frappe


def poll_aggregators():
    """Mirror order status to/from delivery platforms (HungerStation, Jahez, ...)."""
    pass


def nightly_backflush():
    """Batched recipe → stock consumption for outlets in 'Batched' mode."""
    pass
