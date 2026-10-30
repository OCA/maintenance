# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon

from ..hooks import post_init_hook


@tagged("post_install", "-at_install")
class TestPostInitHook(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.equipment_obj = cls.env["maintenance.equipment"]
        cls.plan_obj = cls.env["maintenance.plan"]

    def test_post_init_hook_creates_plan_from_expected_mtbf(self):
        """A plan is created for each equipment with an expected MTBF."""
        equipment = self.equipment_obj.create(
            {"name": "Equipment with MTBF", "expected_mtbf": 30}
        )
        self.assertFalse(equipment.maintenance_plan_ids)

        post_init_hook(self.env)

        plans = self.plan_obj.search([("equipment_id", "=", equipment.id)])
        self.assertEqual(len(plans), 1)
        plan = plans
        # Interval is derived from expected_mtbf, expressed in days.
        self.assertEqual(plan.interval, 30)
        self.assertEqual(plan.interval_step, "day")
        self.assertEqual(plan.maintenance_kind_id.name, "Install")

    def test_post_init_hook_ignores_equipment_without_mtbf(self):
        """Equipment without an expected MTBF gets no plan from the hook."""
        equipment = self.equipment_obj.create({"name": "Equipment without MTBF"})

        post_init_hook(self.env)

        plans = self.plan_obj.search([("equipment_id", "=", equipment.id)])
        self.assertFalse(plans)
