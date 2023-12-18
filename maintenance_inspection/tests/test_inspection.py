# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.maintenance_plan.tests.common import TestMaintenancePlanBase


class TestInspection(TestMaintenancePlanBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.item_1 = cls.env["maintenance.inspection.item"].create(
            {
                "name": "item 01",
            }
        )
        cls.item_2 = cls.env["maintenance.inspection.item"].create(
            {
                "name": "item 02",
            }
        )

    def test_request(self):
        """
        Testing the new flow.
        1 - Setting an inspection
        2 - Setting the value of the inspection
        3 - Closing the inspection
        """
        request = self.env["maintenance.request"].create(
            {
                "name": "Request",
                "maintenance_type": "preventive",
            }
        )
        self.assertFalse(request.has_inspection)
        request.set_inspection()
        self.assertTrue(request.has_inspection)
        self.assertFalse(request.inspection_line_ids)
        request.write({"inspection_line_ids": [(0, 0, {"item_id": self.item_1.id})]})
        self.assertEqual(request.inspection_line_ids.result, "todo")
        request.inspection_line_ids.action_success()
        self.assertEqual(request.inspection_line_ids.result, "success")
        request.inspection_line_ids.action_failure()
        self.assertEqual(request.inspection_line_ids.result, "failure")
        self.assertFalse(request.inspection_closed_at)
        request.finish_inspection()
        self.assertTrue(request.inspection_closed_at)

    def test_plan_no_inspection(self):
        """
        Testing that everything is the same for old fashion data
        """
        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
        self.assertFalse(any(generated_requests.mapped("has_inspection")))

    def test_plan_inspection(self):
        """
        Testing what happens when we create a plan with assigned inspection items:
        Inspection lines should be created
        """
        self.maintenance_plan_1.inspection_item_ids = self.item_1 | self.item_2
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
        self.assertTrue(all(generated_requests.mapped("has_inspection")))
        for request in generated_requests:
            self.assertEqual(2, len(request.inspection_line_ids))
            self.assertIn(self.item_1, request.mapped("inspection_line_ids.item_id"))
            self.assertIn(self.item_2, request.mapped("inspection_line_ids.item_id"))
