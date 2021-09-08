# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

import odoo.tests.common as test_common
from odoo import fields


class TestMaintenancePlanActivity(test_common.TransactionCase):
    def setUp(self):
        super(TestMaintenancePlanActivity, self).setUp()
        self.maintenance_request_obj = self.env["maintenance.request"]
        self.maintenance_plan_obj = self.env["maintenance.plan"]
        self.maintenance_equipment_obj = self.env["maintenance.equipment"]
        self.maintenance_planned_activity_obj = self.env["maintenance.planned.activity"]
        self.mail_activity_obj = self.env["mail.activity"]
        self.cron = self.env.ref("maintenance.maintenance_requests_cron")

        self.equipment_1 = self.maintenance_equipment_obj.create({"name": "Laptop 1"})
        self.call = self.env["mail.activity.type"].search(
            [("name", "=", "Call")], limit=1
        )
        self.maintenance_plan_1 = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        self.planned_activity = self.maintenance_planned_activity_obj.create(
            {
                "maintenance_plan_id": self.maintenance_plan_1.id,
                "activity_type_id": self.call.id,
                "date_before_request": 2,
            }
        )

    def test_01_cron_auto_create_activities(self):
        """Execute cron and check the request and the activities that have
        been created
        """
        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)]
        )
        self.assertEqual(len(generated_requests), 3)
        request_1 = generated_requests[0]
        # Check if activity Call has been created for the request 1
        generated_activities = self.mail_activity_obj.search(
            [("res_id", "=", request_1.id)]
        )
        self.assertEqual(len(generated_activities), 2)
        self.assertEqual(generated_activities[0].activity_type_id.name, self.call.name)
        self.assertEqual(
            generated_activities[0].date_deadline,
            fields.Date.from_string(request_1.schedule_date) - timedelta(days=2),
        )
