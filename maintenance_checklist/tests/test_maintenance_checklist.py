# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestMaintenanceRequest(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.maintenance_request = self.env["maintenance.request"]
        self.equipment_checklist1 = self.env["equipment.checklist"].create(
            {"name": "Equipment Checklist 1", "description": "Description1"}
        )
        self.equipment_checklist2 = self.env["equipment.checklist"].create(
            {"name": "Equipment Checklist 2", "description": "Description2"}
        )
        self.equipment_checklist3 = self.env["equipment.checklist"].create(
            {"name": "Equipment Checklist 3", "description": "Description3"}
        )

    def test_compute(self):
        maintenance_request = self.maintenance_request.create(
            {
                "name": "Test 1",
                "checklist_ids": [
                    (
                        0,
                        0,
                        {
                            "state": "process",
                            "checklist_id": self.equipment_checklist1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "state": "block",
                            "checklist_id": self.equipment_checklist2.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "state": "done",
                            "checklist_id": self.equipment_checklist3.id,
                        },
                    ),
                ],
            }
        )
        self.assertEqual(maintenance_request.completed_checklist, 1)
        self.assertEqual(maintenance_request.inprogress_checklist, 1)
        self.assertEqual(maintenance_request.onhold_checklist, 1)
