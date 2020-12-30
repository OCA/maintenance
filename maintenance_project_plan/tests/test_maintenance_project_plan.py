# Copyright 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import odoo.tests.common as test_common


class TestMaintenanceProjectPlan(test_common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.cron = self.env.ref("maintenance.maintenance_requests_cron")

        self.maintenance_kind_test = self.env["maintenance.kind"].create(
            {"name": "Test kind"}
        )

        self.monitor1 = self.env.ref("maintenance.equipment_monitor1")
        self.monitor1.maintenance_plan_ids = [
            (
                0,
                0,
                {
                    "maintenance_kind_id": self.maintenance_kind_test.id,
                    "duration": 1,
                    "project_id": self.env.ref(
                        "maintenance_project.project_project_1"
                    ).id,
                    "task_id": self.env.ref("maintenance_project.project_task_11").id,
                },
            )
        ]

    def test_prepare_request_from_plan(self):
        self.env["maintenance.request"].search(
            [("maintenance_type", "=", "preventive")]
        ).unlink()  # request cleanup in order to grant test execution
        plans = self.env["maintenance.plan"].search([("project_id", "!=", False)])
        for plan in plans:
            requests = plan.equipment_id._create_new_request(plan)
            self.assertTrue(requests)
            request = requests[0]
            self.assertEqual(request.project_id, plan.project_id)
            self.assertEqual(
                request.task_id,
                plan.task_id or plan.equipment_id.preventive_default_task_id,
            )

    def test_plan_onchange_project(self):
        plan1 = self.env["maintenance.plan"].new(
            {
                "equipment_id": self.env.ref(
                    "maintenance_plan.maintenance_plan_monthly_monitor4"
                ).id,
                "maintenance_kind_id": self.maintenance_kind_test.id,
                "duration": 1,
                "project_id": self.env.ref("maintenance_project.project_project_1").id,
                "task_id": self.env.ref("maintenance_project.project_task_11").id,
            }
        )
        self.assertEqual(
            plan1.project_id, self.env.ref("maintenance_project.project_project_1")
        )
        self.assertEqual(
            plan1.task_id, self.env.ref("maintenance_project.project_task_11")
        )
        plan1.project_id = False
        self.assertFalse(plan1.task_id)

        plan1.project_id = self.env.ref("maintenance_project.project_project_1")
        self.assertFalse(plan1.task_id)
