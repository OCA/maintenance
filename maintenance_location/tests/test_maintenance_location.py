# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMaintenanceLocation(TransactionCase):
    def setUp(self):
        super().setUp()
        self.location_1 = self.env["maintenance.location"].create(
            {"name": "L1"}
        )
        self.location_2 = self.env["maintenance.location"].create(
            {"name": "L2", "parent_id": self.location_1.id}
        )
        self.equipment = self.env["maintenance.equipment"].create(
            {"name": "L2", "location_id": self.location_1.id}
        )
        self.team = self.env["maintenance.team"].create({"name": "Team"})
        self.request = self.env["maintenance.request"].create(
            {"name": "Request", "maintenance_team_id": self.team.id}
        )

    def test_maintenance_location(self):
        self.assertEqual(self.location_2.complete_name, "L1 / L2")
        with self.assertRaises(ValidationError):
            self.location_1.write({"parent_id": self.location_2.id})

        self.request.write({"equipment_id": self.equipment.id})
        self.request._onchange_equipment_id()
        self.assertEqual(self.request.location_id.id, self.location_1.id)
