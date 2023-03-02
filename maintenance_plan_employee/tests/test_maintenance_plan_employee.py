# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.addons.maintenance_plan.tests.common import TestMaintenancePlanBase


class TestMaintenancePlanEmployee(TestMaintenancePlanBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee_a = cls.env["hr.employee"].create({"name": "Test employee A"})
        cls.employee_b = cls.env["hr.employee"].create({"name": "Test employee B"})
        cls.maintenance_plan_1.write(
            {"employee_ids": [(6, 0, [cls.employee_a.id, cls.employee_b.id])]}
        )

    def test_maintenance_reqest_from_plan(self):
        # maintenance_plan_1
        self.maintenance_plan_1.button_manual_request_generation()
        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
            limit=1,
        )
        self.assertIn(self.employee_a, generated_request.employee_ids)
        self.assertIn(self.employee_b, generated_request.employee_ids)
        # report
        res = self.report_obj._get_report_from_name(
            "base_maintenance.report_maintenance_request"
        ).render_qweb_text(generated_request.ids, False)
        self.assertRegex(str(res[0]), "Test employee A")
        self.assertRegex(str(res[0]), "Test employee B")
        # maintenance_plan_2
        self.maintenance_plan_2.button_manual_request_generation()
        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_2.id)],
            order="schedule_date asc",
            limit=1,
        )
        self.assertFalse(generated_request.employee_ids)
