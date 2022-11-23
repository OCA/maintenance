# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, fields
from odoo.tests import common


class TestMaintenancePlan(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(
                self.env.context,
                tracking_disable=True,
            )
        )
        self.maintenance_request_obj = self.env["maintenance.request"]
        self.maintenance_plan_obj = self.env["maintenance.plan"]
        self.maintenance_equipment_obj = self.env["maintenance.equipment"]
        self.cron = self.env.ref("maintenance.maintenance_requests_cron")
        self.weekly_kind = self.env.ref("maintenance_plan.maintenance_kind_weekly")
        self.done_stage = self.env.ref("maintenance.stage_3")

        self.equipment_1 = self.maintenance_equipment_obj.create({"name": "Laptop 1"})
        self.today_date = fields.Date.today()
        self.maintenance_plan_1 = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "start_maintenance_date": self.today_date,
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

    def test_name_get(self):
        self.assertEqual(
            self.maintenance_plan_1.name_get()[0][1],
            _(
                "Unnamed %(void)s plan (%(eqpmnt)s)",
                void="",
                eqpmnt=self.maintenance_plan_1.equipment_id.name,
            ),
        )
        self.assertEqual(
            self.maintenance_plan_2.name_get()[0][1],
            _(
                "Unnamed %(kind)s plan (%(eqpmnt)s)",
                kind=self.maintenance_plan_2.maintenance_kind_id.name,
                eqpmnt=self.maintenance_plan_2.equipment_id.name,
            ),
        )
        self.assertEqual(
            self.maintenance_plan_3.name_get()[0][1], self.maintenance_plan_3.name
        )

    def test_next_maintenance_date_01(self):
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
            self.maintenance_plan_1.next_maintenance_date,
            self.maintenance_plan_1.start_maintenance_date
            + relativedelta(months=self.maintenance_plan_1.interval),
        )

    def test_next_maintenance_date_02(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
        next_maintenance = generated_requests[0]
        next_date = next_maintenance.request_date
        # First maintenance was planned today:
        self.assertEqual(next_date, self.today_date)
        self.assertEqual(
            next_date,
            self.maintenance_plan_1.start_maintenance_date,
        )
        self.assertEqual(
            next_date,
            self.maintenance_plan_1.next_maintenance_date,
        )
        # Complete request:
        next_maintenance.stage_id = self.done_stage
        # Check next one:
        next_maintenance = generated_requests[1]
        next_date = next_maintenance.request_date
        # This should be expected next month:
        self.assertEqual(
            next_date,
            self.today_date + relativedelta(months=self.maintenance_plan_1.interval),
        )
        self.assertEqual(
            next_date,
            self.maintenance_plan_1.next_maintenance_date,
        )
        # Complete request and Check next one:
        next_maintenance.stage_id = self.done_stage
        next_maintenance = generated_requests[2]
        next_date = next_maintenance.request_date
        # This one should be expected in 2 months:
        self.assertEqual(
            next_date,
            self.today_date
            + relativedelta(months=2 * self.maintenance_plan_1.interval),
        )
        self.assertEqual(
            next_date,
            self.maintenance_plan_1.next_maintenance_date,
        )
        # Move it to a date before `start_maintenance_date` (the request should
        # be ignored)
        past_date = self.today_date + relativedelta(
            months=-3 * self.maintenance_plan_1.interval
        )
        next_maintenance.request_date = past_date
        self.assertNotEqual(
            past_date,
            self.maintenance_plan_1.next_maintenance_date,
        )
        self.assertEqual(
            self.maintenance_plan_1.next_maintenance_date,
            self.today_date
            + relativedelta(months=2 * self.maintenance_plan_1.interval),
        )
        # Move the request_date far into the future:
        future_date = self.today_date + relativedelta(
            months=5 * self.maintenance_plan_1.interval
        )
        next_maintenance.request_date = future_date
        self.assertEqual(
            future_date,
            self.maintenance_plan_1.next_maintenance_date,
        )
        # Complete request in that date, next expected date should be 1 month
        # after latest request done.:
        next_maintenance.stage_id = self.done_stage
        self.assertEqual(
            self.maintenance_plan_1.next_maintenance_date,
            self.today_date
            + relativedelta(months=6 * self.maintenance_plan_1.interval),
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
                fields.Date.to_date(req.schedule_date), request_date_schedule
            )
            request_date_schedule = request_date_schedule + relativedelta(months=1)

        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_4.id)], limit=1
        )
        self.assertEqual(
            generated_request.name,
            _(
                "Preventive Maintenance (%(kind)s) - %(plan)s",
                kind=self.weekly_kind.name,
                plan=self.maintenance_plan_4.name,
            ),
        )

    def test_generate_requests2(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 3)

        # We set plan start_maintenanca_date to a future one. New requests should take
        # into account this new date.

        self.maintenance_plan_1.write(
            {
                "start_maintenance_date": fields.Date.to_string(
                    self.today_date + timedelta(weeks=9)
                ),
                "maintenance_plan_horizon": 3,
            }
        )

        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 4)
        self.assertEqual(
            generated_requests[-1].request_date,
            self.today_date + relativedelta(weeks=9),
        )

    def test_get_relativedelta(self):
        plan = self.maintenance_plan_1
        result = plan.get_relativedelta(1, "day")
        self.assertEqual(relativedelta(days=1), result)
        result = plan.get_relativedelta(1, "week")
        self.assertEqual(relativedelta(weeks=1), result)
        result = plan.get_relativedelta(1, "month")
        self.assertEqual(relativedelta(months=1), result)
        result = plan.get_relativedelta(1, "year")
        self.assertEqual(relativedelta(years=1), result)

    def test_generate_requests_inactive_equipment(self):
        self.equipment_1.active = False
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 0)
        self.equipment_1.active = True
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
