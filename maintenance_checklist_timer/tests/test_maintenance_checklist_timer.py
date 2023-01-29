# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestMaintenanceRequest(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.project = self.env["project.project"].create({"name": "My project"})
        self.maintenance_request1 = self.env["maintenance.request"].create(
            {"name": "Request 1", "project_id": self.project.id}
        )
        self.maintenance_request2 = self.env["maintenance.request"].create(
            {"name": "Request 2"}
        )

        self.equipment_checklist1 = self.env["equipment.checklist"].create(
            {"name": "Equipment Checklist 1", "description": "Description1"}
        )
        self.equipment_checklist2 = self.env["equipment.checklist"].create(
            {"name": "Equipment Checklist 2", "description": "Description2"}
        )
        self.maintenance_checklist1 = self.env["maintenance.checklist"].create(
            {
                "name": "Maintenance Checklist 1",
                "checklist_id": self.equipment_checklist1.id,
                "request_id": self.maintenance_request1.id,
            }
        )
        self.maintenance_checklist2 = self.env["maintenance.checklist"].create(
            {
                "name": "Maintenance Checklist 2",
                "checklist_id": self.equipment_checklist2.id,
                "request_id": self.maintenance_request2.id,
            }
        )

    def test_save_timesheet_validation_error(self):
        maintenance_checklist_timesheet = self.env[
            "maintenance.checklist.create.timesheet"
        ].create(
            {
                "time_spent": 1,
                "checklist_id": self.maintenance_checklist2.id,
            }
        )
        with self.assertRaises(ValidationError):
            maintenance_checklist_timesheet.save_timesheet()

    def test_save_timesheet(self):
        maintenance_checklist_timesheet = self.env[
            "maintenance.checklist.create.timesheet"
        ].create(
            {
                "time_spent": 1,
                "checklist_id": self.maintenance_checklist1.id,
            }
        )
        maintenance_checklist_timesheet.save_timesheet()
        self.assertEqual(self.maintenance_checklist1.state, "done")
