# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentSequence(TransactionCase):
    def setUp(self):
        super().setUp()
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
        self.assertEqual(equipment_1.serial_no, "TTC0001")
        # Set code manually
        equipment_1.write({"serial_no": "TTC0023"})
        self.assertEqual(equipment_1.serial_no, "TTC0023")
        # Remove code and be automatically set to sequence next value
        equipment_1.write({"serial_no": False})
        self.assertEqual(equipment_1.serial_no, "TTC0002")

    def test_02_compute_seq_number_next(self):
        """Test Compute 'sequence_number_next' according to the current sequence in use,
        an ir.sequence or an ir.sequence.date_range."""

        sequence = self.sequence_obj.create(
            {
                "name": "Test Sequence",
                "prefix": "TST",
                "padding": 3,
                "number_next": 5,
                "use_date_range": False,
            }
        )

        category = self.maintenance_equipment_categ_obj.create(
            {
                "name": "Test Category with Sequence",
                "sequence_id": sequence.id,
            }
        )

        category._compute_seq_number_next()
        self.assertEqual(category.sequence_number_next, 5)

        sequence.write({"number_next_actual": 10})
        category._compute_seq_number_next()
        self.assertEqual(category.sequence_number_next, 10)

        category_no_seq = self.maintenance_equipment_categ_obj.create(
            {
                "name": "Test Category without Sequence",
            }
        )

        category_no_seq._compute_seq_number_next()
        self.assertEqual(category_no_seq.sequence_number_next, 1)

    def test_03_create_with_existing_sequence(self):
        """Test def create(self, vals):"""

        existing_sequence = self.sequence_obj.create(
            {
                "name": "Existing Sequence",
                "prefix": "EXS",
                "padding": 3,
                "number_increment": 1,
                "use_date_range": False,
            }
        )

        category_with_seq = self.maintenance_equipment_categ_obj.create(
            {
                "name": "Category with Existing Sequence",
                "sequence_id": existing_sequence.id,
            }
        )

        self.assertEqual(category_with_seq.sequence_prefix, "EXS")
        self.assertEqual(category_with_seq.sequence_id.id, existing_sequence.id)

    def test_04_compute_equipment_code(self):
        """Test def _compute_equipment_code(self):"""

        seq_01 = self.sequence_obj.create(
            {
                "name": "Test Sequence",
                "prefix": "TST",
                "padding": 3,
                "number_increment": 1,
                "use_date_range": False,
            }
        )

        cat_01 = self.maintenance_equipment_categ_obj.create(
            {"name": "Test Category", "sequence_id": seq_01.id}
        )

        equipment_01 = self.env["maintenance.equipment"].create(
            {
                "name": "Test Equipment 1",
                "category_id": cat_01.id,
                "serial_no": False,
            }
        )

        equipment_02 = self.env["maintenance.equipment"].create(
            {
                "name": "Test Equipment 2",
                "category_id": cat_01.id,
                "serial_no": False,
            }
        )

        equipment_03 = self.env["maintenance.equipment"].create(
            {
                "name": "Test Equipment 3",
                "category_id": False,
                "serial_no": False,
            }
        )
        self.assertEqual(equipment_01.serial_no, "TST001")
        self.assertEqual(equipment_02.serial_no, "TST002")
        self.assertFalse(equipment_03.serial_no)

        equipment_03.write({"category_id": cat_01.id})
        self.assertEqual(equipment_03.serial_no, "TST003")
