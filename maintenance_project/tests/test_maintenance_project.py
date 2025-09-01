# Copyright 2019 Solvos Consultor??a Inform??tica (<http://www.solvos.es>)
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import Form, new_test_user
from odoo.tests.common import users
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceProject(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project1 = cls.env["project.project"].create({"name": "My project"})
        cls.project_demo = cls.env.ref("maintenance_project.project_project_1")
        cls.milestone = cls.env["project.milestone"].create(
            {"name": "My milestone", "project_id": cls.project1.id}
        )
        new_test_user(
            cls.env,
            login="test-user",
            groups="maintenance.group_equipment_manager,project.group_project_user",
        )
        new_test_user(
            cls.env,
            login="test-project_manager-user",
            groups="maintenance.group_equipment_manager,project.group_project_manager",
        )
        cls.equipment1 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment",
                "maintenance_team_id": cls.env.ref(
                    "maintenance.equipment_team_metrology"
                ).id,
            }
        )
        cls.equipment2 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment without project",
            }
        )
        cls.equipment3 = cls.env["maintenance.equipment"].create(
            {
                "name": "My equipment with related project",
                "project_id": cls.project1.id,
            }
        )
        cls.equipment_demo = cls.env.ref("maintenance_project.equipment_3")

    def test_maintenance_equipment_project_misc(self):
        self.assertFalse(self.equipment1.project_id)
        self.assertFalse(self.equipment2.project_id)
        self.assertEqual(self.equipment3.project_id, self.project1)
        self.assertEqual(self.equipment_demo.name, self.equipment_demo.project_id.name)

    @users("test-project_manager-user")
    def test_maintenance_equipment_project_admin(self):
        equipment_a = self.env["maintenance.equipment"].create(
            {
                "name": "Test equipment A",
            }
        )
        self.assertFalse(equipment_a.project_id)
        equipment_a.action_create_project()
        self.assertTrue(equipment_a.project_id)
        self.assertEqual(equipment_a.name, equipment_a.project_id.name)
        equipment_b = self.env["maintenance.equipment"].create(
            {
                "name": "Test equipment b",
                "project_id": self.project1.id,
            }
        )
        self.assertEqual(equipment_b.project_id, self.project1)
        equipment_b.action_create_project()
        self.assertEqual(equipment_b.project_id, self.project1)

    def test_project_equipment_count(self):
        self.equipment1.action_create_project()
        self.assertEqual(self.project1.equipment_count, 1)
        self.assertEqual(self.equipment1.project_id.equipment_count, 1)
        self.assertEqual(self.project_demo.equipment_count, 2)
        self.assertEqual(self.equipment_demo.project_id.equipment_count, 1)

    @users("test-user")
    def test_request_equipment(self):
        request_form_1 = Form(self.env["maintenance.request"])
        request_form_1.name = "My test request #1"
        self.assertFalse(request_form_1.project_id)
        request_form_1.equipment_id = self.equipment1
        self.assertEqual(request_form_1.project_id, self.equipment1.project_id)
        request_form_2 = Form(self.env["maintenance.request"])
        request_form_2.name = "My test request #2"
        request_form_2.equipment_id = self.equipment2
        self.assertFalse(request_form_2.project_id)

    def test_generate_requests(self):
        req_name = "My new recurring test request"
        req = self.env["maintenance.request"].create(
            {
                "name": req_name,
                "maintenance_type": "preventive",
                "duration": 1.0,
                "recurring_maintenance": True,
                "repeat_interval": 1,
                "repeat_unit": "month",
                "repeat_type": "forever",
            }
        )
        req.equipment_id = self.equipment1
        req.onchange_equipment_id()
        req.description = "Request done!"

        request_obj = self.env["maintenance.request"]
        domain = [
            ("name", "=", req_name),
            ("equipment_id", "=", self.equipment1.id),
            ("project_id", "=", self.equipment1.project_id.id),
        ]
        my_requests = request_obj.search(domain)
        self.assertEqual(len(my_requests), 1)

        req.stage_id = self.env.ref("maintenance.stage_3")
        my_requests = request_obj.search(domain)
        self.assertEqual(len(my_requests), 2)

    def test_project_action_views(self):
        act1 = self.project1.action_view_equipment_ids()
        self.assertEqual(act1["domain"][0][2], self.project1.id)
        self.assertEqual(act1["context"]["default_project_id"], self.project1.id)
        self.assertFalse(act1["context"]["default_create_project_from_equipment"])
        act2 = self.project1.action_view_maintenance_request_ids()
        self.assertEqual(act2["domain"][0][2], self.project1.id)
        self.assertEqual(act2["context"]["default_project_id"], self.project1.id)

    def test_milestones(self):
        req_name = "My new recurring test request"
        req = self.env["maintenance.request"].create(
            {
                "name": req_name,
                "maintenance_type": "preventive",
                "duration": 1.0,
                "recurring_maintenance": True,
                "repeat_interval": 1,
                "repeat_unit": "month",
                "repeat_type": "forever",
                "project_id": self.project1.id,
            }
        )
        self.assertFalse(req.milestone_id)
        self.assertEqual(0, self.milestone.maintenance_request_count)
        task = self.env["project.task"].create(
            {
                "name": "My test task",
                "project_id": self.project1.id,
                "milestone_id": self.milestone.id,
            }
        )
        req.task_id = task
        self.assertEqual(req.milestone_id, self.milestone)
        self.assertEqual(1, self.milestone.maintenance_request_count)
        action = self.milestone.action_view_maintenance_request()
        self.assertIn("res_id", action)
        self.assertEqual(action["res_id"], req.id)
        req2 = self.env["maintenance.request"].create(
            {
                "name": req_name,
                "maintenance_type": "preventive",
                "duration": 1.0,
                "recurring_maintenance": True,
                "repeat_interval": 1,
                "repeat_unit": "month",
                "repeat_type": "forever",
                "project_id": self.project1.id,
                "milestone_id": self.milestone.id,
            }
        )
        self.milestone.invalidate_recordset()
        self.assertEqual(2, self.milestone.maintenance_request_count)
        action = self.milestone.action_view_maintenance_request()
        self.assertFalse(action.get("res_id"))
        milestone_requests = self.env[action["res_model"]].search(
            safe_eval(action["domain"], locals_dict={"active_id": self.milestone.id})
        )
        self.assertEqual(2, len(milestone_requests))
        self.assertIn(req, milestone_requests)
        self.assertIn(req2, milestone_requests)
