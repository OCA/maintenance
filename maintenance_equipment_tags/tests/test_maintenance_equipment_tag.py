from odoo import Command
from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentTag(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag_model = cls.env["maintenance.equipment.tag"]
        cls.equipment_model = cls.env["maintenance.equipment"]

    def test_get_default_color_value_range(self):
        """Check that the default color value is within the range (1 to 15)."""
        color_value = self.tag_model.get_default_color_value()
        self.assertGreaterEqual(color_value, 1)
        self.assertLessEqual(color_value, 15)

    def test_get_default_color_value_is_integer(self):
        """Verify that the method returns an integer value."""
        color_value = self.tag_model.get_default_color_value()
        self.assertIsInstance(color_value, int)

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
