# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command


def uninstall_hook(env):
    """Restore the internal-user access removed from standard menus."""
    menus = env["ir.ui.menu"]
    for xmlid in (
        "maintenance.menu_m_dashboard",
        "maintenance.menu_m_request",
        "maintenance.menu_m_request_form",
        "maintenance.menu_m_request_calendar",
        "maintenance.menu_equipment_form",
        "maintenance.menu_m_reports",
        "maintenance.menu_m_reports_oee",
        "maintenance.menu_m_reports_losses",
    ):
        menu = env.ref(xmlid, raise_if_not_found=False)
        if menu:
            menus |= menu
    menus.write({"group_ids": [Command.link(env.ref("base.group_user").id)]})
