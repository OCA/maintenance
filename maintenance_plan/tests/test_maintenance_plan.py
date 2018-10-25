# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as test_common
from odoo import fields
from datetime import timedelta


class TestMaintenancePlan(test_common.TransactionCase):

    def setUp(self):
        super(TestMaintenancePlan, self).setUp()
        self.printer1 = self.env.ref('maintenance.equipment_printer1')
        self.cron = self.env.ref('maintenance.maintenance_requests_cron')

    def test_next_maintenance_date(self):

        today = fields.Date.today()
        today_date = fields.Date.from_string(today)

        for plan in self.printer1.maintenance_plan_ids:
            self.assertEqual(plan.next_maintenance_date,
                             fields.Date.to_string(
                                 today_date + timedelta(days=plan.period)))

    def test_generate_requests(self):

        self.cron.method_direct_trigger()

        generated_requests = self.env['maintenance.request'].search(
            ['|',
             ('maintenance_kind_id', '=', self.env.ref(
                 'maintenance_plan.maintenance_kind_monthly').id),
             ('maintenance_kind_id', '=', self.env.ref(
                 'maintenance_plan.maintenance_kind_weekly').id)
             ])

        for req in generated_requests:
            for plan in req.equipment_id.maintenance_plan_ids:
                if plan.maintenance_kind_id == req.maintenance_kind_id:
                    self.assertEqual(req.duration, plan.duration)
                    self.assertEqual(req.request_date,
                                     plan.next_maintenance_date)
