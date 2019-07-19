# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as test_common
from odoo import fields
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class TestMaintenancePlan(test_common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.maintenance_request_obj = self.env['maintenance.request']
        self.maintenance_plan_obj = self.env['maintenance.plan']
        self.maintenance_equipment_obj = self.env['maintenance.equipment']
        self.cron = self.env.ref('maintenance.maintenance_requests_cron')

        self.equipment_1 = self.maintenance_equipment_obj.create({
            'name': 'Laptop 1',
        })
        self.maintenance_plan_1 = self.maintenance_plan_obj.create({
            'equipment_id': self.equipment_1.id,
            'interval': 1,
            'interval_step': 'month',
            'maintenance_plan_horizon': 2,
            'planning_step': 'month'
        })

        today = fields.Date.today()
        self.today_date = fields.Date.from_string(today)

    def test_next_maintenance_date(self):
        # We set start maintenance date tomorrow and check next maintenance
        # date has been correctly computed
        self.maintenance_plan_1.write({
            'start_maintenance_date': fields.Date.to_string(
                self.today_date - timedelta(days=1)),
        })
        self.maintenance_plan_1._compute_next_maintenance()
        # Check next maintenance date is 1 month from start date
        self.assertEqual(
            fields.Date.from_string(
                self.maintenance_plan_1.next_maintenance_date),
            fields.Date.from_string(
                self.maintenance_plan_1.start_maintenance_date) +
            relativedelta(months=self.maintenance_plan_1.interval)
        )

    def test_generate_requests(self):
        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [('maintenance_plan_id', '=', self.maintenance_plan_1.id)],
            order="schedule_date asc"
        )
        self.assertEqual(len(generated_requests), 3)

        request_date_schedule = self.today_date

        for req in generated_requests:
            self.assertEqual(fields.Date.from_string(req.schedule_date),
                             request_date_schedule)
            request_date_schedule = \
                request_date_schedule + relativedelta(months=1)
