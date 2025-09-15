# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceEquipmentHierarchy(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Equipment = cls.env["maintenance.equipment"]
        cls.equipment1 = cls.Equipment.create({"name": "Equipment 1"})

        cls.equipment1_1 = cls.Equipment.create({"name": "Equipment 1.1"})
        cls.equipment1_2 = cls.Equipment.create({"name": "Equipment 1.2"})

    def test_01_hierarchy(self):
        self.equipment1_1.parent_id = self.equipment1
        res = self.equipment1.preview_child_list()
        self.assertEqual(res["domain"], [("parent_id", "=", self.equipment1.id)])

    def test_02_recursion(self):
        with self.assertRaises(UserError):
            self.equipment1.parent_id = self.equipment1

    def test_03_name_get_display_complete(self):
        self.equipment1_1.parent_id = self.equipment1
        equipment1_1_complete_name = (
            self.equipment1.name + " / " + self.equipment1_1.name
        )

        self.assertEqual(self.equipment1.name_get()[0][1], self.equipment1.name)
        self.assertEqual(self.equipment1.complete_name, self.equipment1.name)
        self.assertEqual(self.equipment1.display_name, self.equipment1.name)

        self.assertEqual(self.equipment1_1.name_get()[0][1], equipment1_1_complete_name)
        self.assertEqual(self.equipment1_1.complete_name, equipment1_1_complete_name)
        self.assertEqual(self.equipment1_1.display_name, equipment1_1_complete_name)

    def test_04_child_count_computation(self):
        # Set parent-child relationships
        self.equipment1_1.parent_id = self.equipment1
        self.equipment1_2.parent_id = self.equipment1

        # Test the child_count computation
        self.equipment1._compute_child_count()

        # Assert that the child_count is correct (2 children)
        self.assertEqual(self.equipment1.child_count, 2)

        # Remove one child and recompute
        self.equipment1_1.parent_id = False
        self.equipment1._compute_child_count()

        # Assert that the child_count is updated (1 child)
        self.assertEqual(self.equipment1.child_count, 1)
