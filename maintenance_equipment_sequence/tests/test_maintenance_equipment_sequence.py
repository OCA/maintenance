# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentSequence(TransactionCase):
    def setUp(self):
        super(TestMaintenanceEquipmentSequence, self).setUp()
        self.maintenance_equipment_categ_obj = self.env[
            "maintenance.equipment.category"
        ]
        self.maintenance_equipment_obj = self.env["maintenance.equipment"]
        self.sequence_obj = self.env["ir.sequence"]

    def test_01_maintenance_equipment_sequence(self):
        """Create equipment category and check sequence has been
        automatically created, create equipments inside category and check
        sequence number has been set
        """
        # Create category
        categ_1 = self.maintenance_equipment_categ_obj.create(
            {
                "name": "Test Category",
                "sequence_prefix": "TTC",
                "sequence_number_next": 1,
            }
        )
        seq_1 = self.sequence_obj.search(
            [("name", "=", categ_1.name), ("prefix", "=", "TTC")], limit=1
        )
        self.assertEqual(seq_1.prefix, categ_1.sequence_prefix)
        self.assertEqual(seq_1.number_next_actual, categ_1.sequence_number_next)

        # Create category without sequence, then write prefix and number next
        categ_2 = self.maintenance_equipment_categ_obj.create(
            {"name": "Test Category 2"}
        )
        categ_2.write({"sequence_prefix": "TTC2", "sequence_number_next": 100})
        seq_2 = self.sequence_obj.search(
            [("name", "=", categ_2.name), ("prefix", "=", "TTC2")], limit=1
        )
        self.assertEqual(seq_2.prefix, categ_2.sequence_prefix)
        self.assertEqual(seq_2.number_next_actual, categ_2.sequence_number_next)

        # Assign sequence 1 to category 2
        categ_2.write({"sequence_id": seq_1.id})
        categ_2._onchange_sequence_id()

        # Create equipment inside category
        equipment_1 = self.maintenance_equipment_obj.create(
            {"name": "Laptop 1", "category_id": categ_2.id}
        )
        categ_2._compute_equipment_code()
        self.assertEqual(equipment_1.code, "TTC0001")
        # Set code manually
        equipment_1.write({"code": "TTC0023"})
        self.assertEqual(equipment_1.code, "TTC0023")
        # Remove code and be automatically set to sequence next value
        equipment_1.write({"code": False})
        self.assertEqual(equipment_1.code, "TTC0002")
