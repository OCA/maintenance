from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceEquipment(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test categories
        cls.category_1 = cls.env["maintenance.equipment.category"].create(
            {"name": "Category 1"}
        )
        cls.category_2 = cls.env["maintenance.equipment.category"].create(
            {"name": "Category 2"}
        )

        # Create test equipment statuses
        cls.status_1 = cls.env["maintenance.equipment.status"].create(
            {
                "name": "Status 1",
                "sequence": 10,
                "category_ids": [Command.set([cls.category_1.id])],
            }
        )
        cls.status_2 = cls.env["maintenance.equipment.status"].create(
            {
                "name": "Status 2",
                "sequence": 20,
                "category_ids": [Command.set([cls.category_1.id])],
            }
        )

    def test_equipment_status_behavior(self):
        # Check status is linked correctly to equipment
        equipment = self.env["maintenance.equipment"].create(
            {
                "name": "Equipment 1",
                "status_id": self.status_1.id,
            }
        )
        self.assertEqual(equipment.status_id, self.status_1)
        self.assertEqual(equipment.status_id.name, "Status 1")

        # Check categories in status
        self.assertIn(self.category_1, self.status_1.category_ids)
        self.assertNotIn(self.category_2, self.status_1.category_ids)

        # Check default active value
        status_3 = self.env["maintenance.equipment.status"].create(
            {
                "name": "Status 3",
            }
        )
        self.assertTrue(status_3.active, "The status should be active by default")

        # Check explicit inactive value
        status_4 = self.env["maintenance.equipment.status"].create(
            {
                "name": "Status 4",
                "active": False,
            }
        )
        self.assertFalse(status_4.active, "The status should be inactive")

        # Check sequences
        self.assertEqual(self.status_1.sequence, 10)
        self.assertEqual(self.status_2.sequence, 20)
