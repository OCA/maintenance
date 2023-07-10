# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common, new_test_user
from odoo.tests.common import users


class TestMaintenanceSecurity(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        cls.user = new_test_user(
            cls.env,
            login="test-basic-user",
        )
        cls.manager = new_test_user(
            cls.env,
            login="test-maintenance-user",
            groups="maintenance.group_equipment_manager",
        )
        cls.category = cls.env["maintenance.equipment.category"].create(
            {"name": "Test category"}
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "Test equipment",
                "category_id": cls.category.id,
            }
        )
        cls.maintenance_menus = [
            cls.env.ref("maintenance.menu_maintenance_title"),
            cls.env.ref("maintenance.menu_m_dashboard"),
            cls.env.ref("maintenance.menu_m_request"),
            cls.env.ref("maintenance.menu_m_request_form"),
            cls.env.ref("maintenance.menu_m_request_calendar"),
            cls.env.ref("maintenance.menu_equipment_form"),
        ]

    def test_maintenance_equipment_full(self):
        mt_mat_assign = self.env.ref("maintenance.mt_mat_assign")
        # Change to manager (with mt_mat_assign subtype)
        self.equipment.write({"owner_user_id": self.manager.id})
        self.assertNotIn(
            self.user.partner_id,
            self.equipment.message_follower_ids.mapped("partner_id"),
        )
        follower = self.equipment.message_follower_ids.filtered(
            lambda x: x.partner_id == self.manager.partner_id
        )
        self.assertIn(mt_mat_assign, follower.subtype_ids)
        # Change to user (without mt_mat_assign subtype)
        self.equipment.write({"owner_user_id": self.user.id})
        follower = self.equipment.message_follower_ids.filtered(
            lambda x: x.partner_id == self.user.partner_id
        )
        self.assertNotIn(mt_mat_assign, follower.subtype_ids)

    @users("test-basic-user")
    def test_ir_ui_menu_user(self):
        items = self.env["ir.ui.menu"]._visible_menu_ids()
        for maintenance_menu in self.maintenance_menus:
            self.assertFalse(maintenance_menu.id in items)

    @users("test-maintenance-user")
    def test_ir_ui_menu_manager(self):
        items = self.env["ir.ui.menu"]._visible_menu_ids()
        for maintenance_menu in self.maintenance_menus:
            self.assertTrue(maintenance_menu.id in items)
