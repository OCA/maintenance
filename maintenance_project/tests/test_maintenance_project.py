# Copyright 2019 Solvos Consultor??a Inform??tica (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import odoo.tests.common as test_common


class TestMaintenanceProject(test_common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestMaintenanceProject, cls).setUpClass()

        cls.cron = cls.env.ref("maintenance.maintenance_requests_cron")
        cls.project1 = cls.env["project.project"].create({"name": "My project"})
        cls.project_demo1 = cls.env.ref("maintenance_project.project_project_1")

        cls.equipment1 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment",
                "create_project_from_equipment": True,
                "maintenance_team_id": cls.env.ref(
                    "maintenance.equipment_team_metrology"
                ).id,
                "period": 30,
                "maintenance_duration": 1.0,
            }
        )
        cls.equipment2 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment without project",
                "create_project_from_equipment": False,
            }
        )
        cls.equipment3 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment with related project",
                "create_project_from_equipment": False,
                "project_id": cls.project1.id,
            }
        )

        cls.equipment_demo1 = cls.env.ref("maintenance_project.equipment_1")
        cls.equipment_demo2 = cls.env.ref("maintenance_project.equipment_2")
        cls.equipment_demo3 = cls.env.ref("maintenance_project.equipment_3")

    def test_maintenance_equipment_project(self):
        self.assertEqual(self.equipment1.name, self.equipment1.project_id.name)
        self.assertFalse(self.equipment2.project_id)
        self.assertEqual(self.equipment3.project_id, self.project1)
        self.assertEqual(
            self.equipment_demo3.name, self.equipment_demo3.project_id.name
        )

    def test_project_equipment_count(self):
        self.assertEqual(self.project1.equipment_count, 1)
        self.assertEqual(self.equipment1.project_id.equipment_count, 1)
        self.assertEqual(self.project_demo1.equipment_count, 2)
        self.assertEqual(self.equipment_demo3.project_id.equipment_count, 1)

    def test_request_onchange_equipment(self):
        req1 = self.env["maintenance.request"].new({"name": "My test request #1"})
        self.assertFalse(req1.project_id)
        req1.equipment_id = self.equipment1
        req1.onchange_equipment_id()
        self.assertEqual(req1.project_id, self.equipment1.project_id)

        req2 = self.env["maintenance.request"].new({"name": "My test request #2"})
        req2.equipment_id = self.equipment2
        req2.onchange_equipment_id()
        self.assertFalse(req2.project_id)

    def test_generate_requests(self):
        self.cron.method_direct_trigger()

        generated_requests = self.env["maintenance.request"].search(
            [("project_id", "!=", False)]
        )
        for req in generated_requests:
            self.assertEqual(req.project_id, req.equipment_id.project_id)
            self.assertEqual(req.task_id, req.equipment_id.preventive_default_task_id)
            self.assertEqual(req.project_id.maintenance_request_count, 1)

    def test_action_views(self):
        act1 = self.project1.action_view_equipment_ids()
        self.assertEqual(act1["domain"][0][2], self.project1.id)
        self.assertEqual(act1["context"]["default_project_id"], self.project1.id)
        self.assertFalse(act1["context"]["default_create_project_from_equipment"])

        act2 = self.project1.action_view_maintenance_request_ids()
        self.assertEqual(act2["domain"][0][2], self.project1.id)
        self.assertEqual(act2["context"]["default_project_id"], self.project1.id)
