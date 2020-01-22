# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from dateutil.relativedelta import relativedelta

import odoo.tests.common as test_common
from odoo import _, fields


class TestMaintenancePlan(test_common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.maintenance_request_obj = self.env["maintenance.request"]
        self.maintenance_plan_obj = self.env["maintenance.plan"]
        self.maintenance_equipment_obj = self.env["maintenance.equipment"]
        self.cron = self.env.ref("maintenance.maintenance_requests_cron")
        self.weekly_kind = self.env.ref("maintenance_plan.maintenance_kind_weekly")

        self.equipment_1 = self.maintenance_equipment_obj.create({"name": "Laptop 1"})
        self.maintenance_plan_1 = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        self.maintenance_plan_2 = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "maintenance_kind_id": self.weekly_kind.id,
                "interval": 1,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        self.maintenance_plan_3 = self.maintenance_plan_obj.create(
            {
                "name": "My custom plan",
                "equipment_id": self.equipment_1.id,
                "interval": 2,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        self.maintenance_plan_4 = self.maintenance_plan_obj.create(
            {
                "name": "Plan without equipment",
                "maintenance_kind_id": self.weekly_kind.id,
                "interval": 1,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )

        today = fields.Date.today()
        self.today_date = fields.Date.from_string(today)

    def test_name_get(self):
        self.assertEqual(
            self.maintenance_plan_1.name_get()[0][1],
            _("Unnamed %s plan (%s)") % ("", self.maintenance_plan_1.equipment_id.name),
        )
        self.assertEqual(
            self.maintenance_plan_2.name_get()[0][1],
            _("Unnamed %s plan (%s)")
            % (
                self.maintenance_plan_2.maintenance_kind_id.name,
                self.maintenance_plan_2.equipment_id.name,
            ),
        )
        self.assertEqual(
            self.maintenance_plan_3.name_get()[0][1], self.maintenance_plan_3.name
        )

    def test_next_maintenance_date(self):
        # We set start maintenance date tomorrow and check next maintenance
        # date has been correctly computed
        self.maintenance_plan_1.write(
            {
                "start_maintenance_date": fields.Date.to_string(
                    self.today_date - timedelta(days=1)
                )
            }
        )
        self.maintenance_plan_1._compute_next_maintenance()
        # Check next maintenance date is 1 month from start date
        self.assertEqual(
            fields.Date.from_string(self.maintenance_plan_1.next_maintenance_date),
            fields.Date.from_string(self.maintenance_plan_1.start_maintenance_date)
            + relativedelta(months=self.maintenance_plan_1.interval),
        )

    def test_generate_requests(self):
        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)

        request_date_schedule = self.today_date

        for req in generated_requests:
            self.assertEqual(
                fields.Date.from_string(req.schedule_date), request_date_schedule
            )
            request_date_schedule = request_date_schedule + relativedelta(months=1)

        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_4.id)], limit=1
        )
        self.assertEqual(
            generated_request.name,
            _("Preventive Maintenance (%s) - %s")
            % (self.weekly_kind.name, self.maintenance_plan_4.name),
        )
