# Copyright 2022-2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form, new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceEquipmentUsage(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env,
            login="test_basic_user",
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {"name": "Test equipment"}
        )
        cls.equipment_usage = cls._create_equipment_usage(cls)

    def _create_equipment_usage(self):
        equipment_usage_form = Form(self.env["maintenance.equipment.usage"])
        equipment_usage_form.equipment_id = self.equipment
        equipment_usage_form.user_id = self.user
        return equipment_usage_form.save()

    def test_maintenance_equipment_full_process(self):
        self.assertIn(self.equipment_usage, self.equipment.usage_ids)
        self.assertFalse(self.equipment.in_use)
        self.assertEqual(self.equipment_usage.state, "draft")
        self.equipment_usage.action_pick()
        self.assertTrue(self.equipment_usage.date_picking)
        self.assertEqual(self.equipment_usage.state, "in_use")
        self.assertTrue(self.equipment.in_use)
        self.equipment_usage.action_return()
        self.assertEqual(self.equipment_usage.state, "returned")
        self.assertTrue(self.equipment_usage.date_return)
        self.assertFalse(self.equipment.in_use)

    def test_maintenance_equipment_cancel_process(self):
        self.assertEqual(self.equipment_usage.state, "draft")
        self.equipment_usage.action_cancel()
        self.assertEqual(self.equipment_usage.state, "cancel")

    def test_maintenance_equipment_multi(self):
        self.equipment_usage.action_pick()
        self.assertEqual(self.equipment_usage.state, "in_use")
        equipment_usage2 = self._create_equipment_usage()
        with self.assertRaises(UserError):
            equipment_usage2.action_pick()
        self.equipment_usage.action_cancel()
        self.assertEqual(self.equipment_usage.state, "cancel")
        equipment_usage2.action_pick()
        self.assertEqual(equipment_usage2.state, "in_use")
