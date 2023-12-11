# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from freezegun import freeze_time

import odoo.tests.common as test_common


class TestMaintenancePlanBase(test_common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # HACK https://github.com/spulec/freezegun/issues/485
        freezer = freeze_time("2023-01-25 15:30:00")
        freezer.__enter__()
        cls.addClassCleanup(freezer.__exit__)
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.maintenance_request_obj = cls.env["maintenance.request"]
        cls.maintenance_plan_obj = cls.env["maintenance.plan"]
        cls.maintenance_equipment_obj = cls.env["maintenance.equipment"]
        cls.cron = cls.env.ref("maintenance.maintenance_requests_cron")
        cls.weekly_kind = cls.env.ref("maintenance_plan.maintenance_kind_weekly")
        cls.done_stage = cls.env.ref("maintenance.stage_3")

        cls.equipment_1 = cls.maintenance_equipment_obj.create({"name": "Laptop 1"})
        cls.maintenance_plan_1 = cls.maintenance_plan_obj.create(
            {
                "equipment_id": cls.equipment_1.id,
                "start_maintenance_date": "2023-01-25",
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        cls.maintenance_plan_2 = cls.maintenance_plan_obj.create(
            {
                "equipment_id": cls.equipment_1.id,
                "maintenance_kind_id": cls.weekly_kind.id,
                "interval": 1,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        cls.maintenance_plan_3 = cls.maintenance_plan_obj.create(
            {
                "name": "My custom plan",
                "equipment_id": cls.equipment_1.id,
                "interval": 2,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        cls.maintenance_plan_4 = cls.maintenance_plan_obj.create(
            {
                "name": "Plan without equipment",
                "maintenance_kind_id": cls.weekly_kind.id,
                "interval": 1,
                "interval_step": "week",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        cls.maintenance_plan_5 = cls.maintenance_plan_obj.create(
            {
                "start_maintenance_date": "2023-01-25",
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
            }
        )
        cls.report_obj = cls.env["ir.actions.report"]
