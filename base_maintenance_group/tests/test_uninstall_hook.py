# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import TransactionCase, tagged

from odoo.addons.base_maintenance_group.hooks import uninstall_hook


@tagged("post_install", "-at_install")
class TestUninstallHook(TransactionCase):
    def test_restore_internal_user_access(self):
        internal_group = self.env.ref("base.group_user")
        other_group = self.env["res.groups"].create({"name": "Other menu access"})
        menus = self.env["ir.ui.menu"]
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
            menu = self.env.ref(xmlid)
            self.assertNotIn(internal_group, menu.group_ids)
            menus |= menu
        menus.write({"group_ids": [Command.link(other_group.id)]})
        original_groups = {menu.id: menu.group_ids for menu in menus}

        uninstall_hook(self.env)
        for menu in menus:
            self.assertEqual(menu.group_ids, original_groups[menu.id] | internal_group)

        # Repeating the hook must leave the same groups in place (idempotency).
        uninstall_hook(self.env)
        for menu in menus:
            self.assertEqual(menu.group_ids, original_groups[menu.id] | internal_group)

    def test_missing_menu_xmlid(self):
        internal_group = self.env.ref("base.group_user")
        missing_menu = self.env.ref("maintenance.menu_m_dashboard")
        other_menu = self.env.ref("maintenance.menu_m_request")
        self.env["ir.model.data"].search(
            [("module", "=", "maintenance"), ("name", "=", "menu_m_dashboard")]
        ).unlink()

        uninstall_hook(self.env)

        self.assertNotIn(internal_group, missing_menu.group_ids)
        self.assertIn(internal_group, other_menu.group_ids)
