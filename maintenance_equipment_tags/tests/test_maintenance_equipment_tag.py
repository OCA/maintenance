from odoo import Command
from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentTag(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag_model = cls.env["maintenance.equipment.tag"]
        cls.equipment_model = cls.env["maintenance.equipment"]

    def test_equipment_tag_color(self):
        """Test tag color assignment."""
        tag = self.tag_model.create({"name": "Test Tag", "color": 5})
        self.assertIsInstance(tag.color, int)
        self.assertEqual(tag.color, 5)

    def test_equipment_tag_assignment(self):
        """Test assigning tags to maintenance equipment."""
        tag = self.tag_model.create({"name": "Test Tag"})
        equipment = self.equipment_model.create(
            {
                "name": "Test Equipment",
                "tag_ids": [Command.link(tag.id)],
            }
        )
        self.assertIn(tag, equipment.tag_ids)
        self.assertIn(equipment, tag.equipment_ids)
