# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo.addons.maintenance_plan.tests.common import TestMaintenancePlanBase


class TestMaintenancePlanDomain(TestMaintenancePlanBase):
    def test_generate_requests_no_domain(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_5.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 3)
        self.assertFalse(generated_requests.mapped("equipment_id"))

    def test_generate_requests_domain(self):
        equipment_2 = self.maintenance_equipment_obj.create({"name": "Laptop 2"})
        self.maintenance_plan_5.write(
            {
                "generate_with_domain": True,
                "generate_domain": json.dumps(
                    [("id", "in", [equipment_2.id, self.equipment_1.id])]
                ),
            }
        )
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_5.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 6)
        self.assertIn(equipment_2, generated_requests.mapped("equipment_id"))
        self.assertIn(self.equipment_1, generated_requests.mapped("equipment_id"))
