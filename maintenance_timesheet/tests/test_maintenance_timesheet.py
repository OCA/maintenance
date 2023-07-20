# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestMaintenanceTimesheet(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.stage_undone = cls.env.ref("maintenance.stage_0")
        cls.stage_done = cls.env.ref("maintenance.stage_4")

        cls.request_demo1 = cls.env.ref("maintenance_timesheet.request_1")
        cls.request2 = cls.env["maintenance.request"].create(
            {
                "name": "Corrective #2 for Generic Monitor",
                "equipment_id": cls.env.ref("maintenance_project.equipment_1").id,
                "user_id": cls.env.ref("base.user_admin").id,
                "schedule_date": fields.Date.today(),
                "stage_id": cls.stage_undone.id,
                "maintenance_type": "corrective",
            }
        )
        cls.timesheet21_data = {
            "name": "Some tasks done",
            "project_id": cls.request2.project_id.id,
            "user_id": cls.env.ref("base.user_admin").id,
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
        ts1.maintenance_request_id = self.request2
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
        data = self.env["maintenance.equipment"]._prepare_project_from_equipment_values(
            {"name": "my name"}
        )
        self.assertTrue(data["allow_timesheets"])
