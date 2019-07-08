# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as test_common
from odoo import fields
from datetime import timedelta


class TestMaintenancePlan(test_common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.printer1 = self.env.ref('maintenance.equipment_printer1')
        self.monitor1 = self.env.ref('maintenance.equipment_monitor1')
        self.cron = self.env.ref('maintenance.maintenance_requests_cron')

        self.kind_quarterly = self.env['maintenance.kind'].create({
            'name': 'Quarterly',
            'active': True,
        })
        self.monitor1.maintenance_plan_ids = [(0, 0, {
            'maintenance_kind_id': self.kind_quarterly.id,
            'period': 90,
            'duration': 3
        })]

    def test_next_maintenance_date(self):

        today = fields.Date.today()

        plan_ids = self.printer1.maintenance_plan_ids + \
            self.monitor1.maintenance_plan_ids
        for plan in plan_ids:
            self.assertEqual(plan.next_maintenance_date,
                             today + timedelta(days=plan.period))

    def test_generate_requests(self):

        self.cron.method_direct_trigger()

        generated_requests = self.env['maintenance.request'].search(
            [('maintenance_kind_id', 'in', [
                self.env.ref('maintenance_plan.maintenance_kind_monthly').id,
                self.env.ref('maintenance_plan.maintenance_kind_weekly').id,
                self.kind_quarterly.id])])

        for req in generated_requests:
            for plan in req.equipment_id.maintenance_plan_ids:
                if plan.maintenance_kind_id == req.maintenance_kind_id:
                    self.assertEqual(req.duration, plan.duration)
                    self.assertEqual(req.request_date,
                                     plan.next_maintenance_date)
