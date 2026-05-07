# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, new_test_user


class TestMaintenanceTimesheet(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.stage_undone = cls.env.ref("maintenance.stage_0")
        cls.stage_done = cls.env.ref("maintenance.stage_4")
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.user_demo = new_test_user(
            cls.env,
            login="test_demo",
            name="Test User Demo",
            groups="base.group_user,hr_timesheet.group_hr_timesheet_user",
        )

        cls.employee_demo = cls.env["hr.employee"].create(
            {
                "name": "Test Employee Demo",
                "user_id": cls.user_demo.id,
                "company_id": cls.env.company.id,
            }
        )

        yesterday = fields.Date.today() - timedelta(days=1)
        assign_date = fields.Date.today().replace(day=10)

        cls.project_1 = cls.env["project.project"].create(
            {
                "name": "General equipment project",
                "user_id": cls.user_admin.id,
            }
        )

        cls.task_11 = cls.env["project.task"].create(
            {
                "name": "General task",
                "project_id": cls.project_1.id,
                "user_ids": [(4, cls.user_admin.id)],
            }
        )

        cls.task_12 = cls.env["project.task"].create(
            {
                "name": "Default preventive task",
                "project_id": cls.project_1.id,
                "user_ids": [(4, cls.user_admin.id)],
            }
        )

        cls.cat_monitor = cls.env["maintenance.equipment.category"].create(
            {"name": "Monitor"}
        )
        cls.cat_computer = cls.env["maintenance.equipment.category"].create(
            {"name": "Computer"}
        )
        cls.maintenance_team = cls.env["maintenance.team"].create(
            {"name": "Test Maintenance Team"}
        )

        cls.equipment_1 = cls.env["maintenance.equipment"].create(
            {
                "name": "Generic Monitor",
                "category_id": cls.cat_monitor.id,
                "owner_user_id": cls.user_admin.id,
                "technician_user_id": cls.user_admin.id,
                "assign_date": assign_date,
                "serial_no": "S/N 1",
                "model": "MODEL1",
                "project_id": cls.project_1.id,
            }
        )

        cls.equipment_2 = cls.env["maintenance.equipment"].create(
            {
                "name": "Generic Monitor with preventive",
                "category_id": cls.cat_monitor.id,
                "owner_user_id": cls.user_admin.id,
                "technician_user_id": cls.user_admin.id,
                "maintenance_team_id": cls.maintenance_team.id,
                "assign_date": assign_date,
                "serial_no": "S/N 2",
                "model": "MODEL2",
                "project_id": cls.project_1.id,
                "preventive_default_task_id": cls.task_12.id,
            }
        )

        cls.equipment_3 = cls.env["maintenance.equipment"].create(
            {
                "name": "Generic Computer with own project",
                "category_id": cls.cat_computer.id,
                "owner_user_id": cls.user_admin.id,
                "technician_user_id": cls.user_admin.id,
                "assign_date": assign_date,
                "serial_no": "S/N 3",
                "model": "MODEL3",
            }
        )

        cls.equipment_3.action_create_project()

        cls.request_demo1 = cls.env["maintenance.request"].create(
            {
                "name": "Corrective #1 for Generic Monitor",
                "equipment_id": cls.equipment_1.id,
                "schedule_date": yesterday,
                "user_id": cls.user_admin.id,
                "project_id": cls.project_1.id,
                "task_id": cls.task_12.id,
                "maintenance_type": "corrective",
            }
        )

        cls.timesheet_11 = cls.env["account.analytic.line"].create(
            {
                "date": yesterday,
                "name": "Request tasks done",
                "maintenance_request_id": cls.request_demo1.id,
                "user_id": cls.user_admin.id,
                "project_id": cls.project_1.id,
                "task_id": cls.task_12.id,
                "unit_amount": 2.0,
            }
        )

        cls.m_request_8 = cls.env["maintenance.request"].create(
            {
                "name": "Maintenance Request 8",
                "project_id": cls.project_1.id,
                "task_id": cls.task_11.id,
                "planned_hours": 1,
            }
        )

        cls.timesheet_21 = cls.env["account.analytic.line"].create(
            {
                "date": yesterday,
                "name": "Touchpad repaired",
                "maintenance_request_id": cls.m_request_8.id,
                "user_id": cls.user_demo.id,
                "project_id": cls.project_1.id,
                "task_id": cls.task_11.id,
                "unit_amount": 3.0,
            }
        )

        cls.request2 = cls.env["maintenance.request"].create(
            {
                "name": "Corrective #2 for Generic Monitor",
                "equipment_id": cls.equipment_1.id,
                "user_id": cls.user_admin.id,
                "schedule_date": fields.Date.today(),
                "stage_id": cls.stage_undone.id,
                "maintenance_type": "corrective",
                "planned_hours": 20,
            }
        )

        cls.timesheet21_data = {
            "name": "Some tasks done",
            "project_id": cls.request2.project_id.id,
            "user_id": cls.user_admin.id,
            "date": fields.Date.today(),
            "unit_amount": 1.5,
        }
        cls.request2.timesheet_ids = [(0, 0, cls.timesheet21_data)]

    def test_request_timesheets(self):
        self.assertEqual(self.request_demo1.timesheet_total_hours, 2)
        self.assertEqual(
            self.request2.timesheet_total_hours, self.timesheet21_data["unit_amount"]
        )

    def test_onchange_maintenance_request_id(self):
        ts1 = self.env["account.analytic.line"].new(
            {
                "date": fields.Date.today(),
                "name": "Timesheet without initial equipment",
                "user_id": self.env.ref("base.user_admin").id,
            }
        )
        self.assertFalse(ts1.project_id)
        ts1.write({"maintenance_request_id": self.request2.id})

        ts1.onchange_maintenance_request_id()
        self.assertEqual(ts1.project_id, self.request2.project_id)
        ts1.project_id = self.project_1
        ts1.onchange_maintenance_request_id()
        self.assertEqual(ts1.project_id, self.request2.project_id)

    def test_check_request_done(self):
        self.request2.stage_id = self.stage_done
        with self.assertRaises(ValidationError):
            self.request2.timesheet_ids = [
                (
                    0,
                    0,
                    {
                        "name": "Attempt to create a task for a done request",
                        "project_id": self.request2.project_id.id,
                        "user_id": self.env.ref("base.user_admin").id,
                        "date": fields.Date.today(),
                        "unit_amount": 2,
                    },
                )
            ]
        with self.assertRaises(ValidationError):
            self.env["account.analytic.line"].create(
                {
                    "name": "Attepting to create a task 2",
                    "project_id": self.request2.project_id.id,
                    "user_id": self.env.ref("base.user_admin").id,
                    "maintenance_request_id": self.request2.id,
                    "date": fields.Date.today(),
                    "unit_amount": 1,
                }
            )
        with self.assertRaises(ValidationError):
            # Attempt to modify a timesheet related a done request
            for timesheet in self.request2.timesheet_ids:
                timesheet.unit_amount += 1
        with self.assertRaises(ValidationError):
            # Attempt to delete a timesheet related a done request
            self.request2.timesheet_ids.unlink()

        self.request2.stage_id = self.stage_undone
        # Deleting timesheets is enabled again
        self.request2.timesheet_ids.unlink()

    def test_action_view_timesheet_ids(self):
        act1 = self.request2.action_view_timesheet_ids()
        self.assertEqual(act1["domain"][0][2], self.request2.id)
        self.assertEqual(
            act1["context"]["default_project_id"], self.request2.project_id.id
        )
        self.assertFalse(act1["context"]["default_task_id"])
        self.assertFalse(act1["context"]["readonly_employee_id"])

    def test_prepare_project_from_equipment_values(self):
        equipment = self.env["maintenance.equipment"].create({"name": "Test equipment"})
        equipment.action_create_project()
        self.assertTrue(equipment.project_id.allow_timesheets)
