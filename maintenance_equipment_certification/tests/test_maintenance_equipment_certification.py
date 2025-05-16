# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentCertification(TransactionCase):
    def setUp(self):
        super().setUp()
        self.equipment = self.env["maintenance.equipment"].create(
            {
                "name": "Test equipment",
            }
        )
        self.user_demo = self.env["res.users"].create(
            {
                "name": "Demo User",
                "login": "Demo",
                "email": "demo@user.com",
                "groups_id": [
                    (6, 0, [self.env.ref("base.group_user").id]),
                ],
            }
        )

    def test_user_with_no_permission(self):
        """Test user with no permission can not modify equipment."""
        with self.assertRaises(AccessError):
            self.equipment.with_user(self.user_demo).name = "Test equipment rename"

    def test_user_with_permission(self):
        """Test user with permission can modify equipment."""
        self.user_demo.write(
            {
                "groups_id": [
                    (6, 0, [self.env.ref("maintenance.group_equipment_manager").id])
                ],
            }
        )
        self.equipment.with_user(self.user_demo).name = "Test equipment rename"
        self.assertEqual(self.equipment.name, "Test equipment rename")
