# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestMaintenanceLocationHr(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {
                "login": "demo_maintenance_location_hr",
                "name": "Demo maintenance location HR",
            }
        )
        cls.location_1 = cls.env["maintenance.location"].create(
            {"name": "L1", "owner_id": cls.user.id}
        )
        cls.equipment = cls.env["maintenance.equipment"].create({"name": "Equipment"})

    def test_maintenance_location(self):
        self.assertNotEqual(self.user, self.equipment.owner_user_id)
        self.equipment.write(
            {"equipment_assign_to": "location", "location_id": self.location_1}
        )
        self.assertEqual(self.user, self.equipment.owner_user_id)
