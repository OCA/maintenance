# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields

from .common import TestMaintenancePlanBase


class TestMaintenancePlanCompany(TestMaintenancePlanBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today_date = fields.Date.from_string("2023-01-25")
        # Create equipment and plan without company
        cls.equipment_no_company = cls.maintenance_equipment_obj.create(
            {"name": "Shared Equipment", "company_id": False}
        )
        cls.plan_no_company = cls.maintenance_plan_obj.create(
            {
                "name": "Shared Plan",
                "equipment_id": cls.equipment_no_company.id,
                "company_id": False,
                "start_maintenance_date": "2023-01-25",
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )

    def test_generate_requests_no_company_on_plan_and_equipment(self):
        # Requests must be created when both plan and equipment have no company
        # The fallback to self.env.company must supply the required value
        self.assertFalse(self.equipment_no_company.company_id)
        self.assertFalse(self.plan_no_company.company_id)
        # This must not raise (company_id is required on maintenance.request)
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.plan_no_company.id)],
            order="schedule_date asc",
        )
        self.assertTrue(generated_requests)
        for request in generated_requests:
            self.assertEqual(request.company_id, self.env.company)

    def test_generate_requests_no_company_on_equipment_only(self):
        # When equipment has no company but plan does, the plan's
        # company should be used
        equipment = self.maintenance_equipment_obj.create(
            {"name": "Company Equipment", "company_id": False}
        )
        plan_with_company = self.maintenance_plan_obj.create(
            {
                "name": "Plan without company",
                "equipment_id": equipment.id,
                "start_maintenance_date": "2023-01-25",
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        self.assertFalse(equipment.company_id)
        self.assertTrue(plan_with_company.company_id)
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", plan_with_company.id)],
            order="schedule_date asc",
        )
        self.assertTrue(generated_requests)
        for request in generated_requests:
            self.assertEqual(
                request.company_id,
                plan_with_company.company_id,
            )
