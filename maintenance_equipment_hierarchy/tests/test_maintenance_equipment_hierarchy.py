# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestMaintenanceEquipmentHierarchy(common.TransactionCase):

    def setUp(self):
        super(TestMaintenanceEquipmentHierarchy, self).setUp()
        self.Equipment = self.env['maintenance.equipment']
        self.equipment1 = self.Equipment.create({
            'name': 'Equipment 1',
        })

        self.equipment1_1 = self.Equipment.create({
            'name': 'Equipment 1.1',
        })

    def test_01_hierarchy(self):
        self.equipment1_1.parent_id = self.equipment1
        res = self.equipment1.preview_child_list()
        self.assertEqual(res['domain'], [('id', 'in', self.equipment1_1.ids)])

    def test_02_recursion(self):
        with self.assertRaises(ValidationError):
            self.equipment1.parent_id = self.equipment1

    def test_03_name_get_display_complete(self):
        self.equipment1_1.parent_id = self.equipment1
        equipment1_1_complete_name = \
            self.equipment1.name + " / " + self.equipment1_1.name

        self.assertEqual(
            self.equipment1.name_get()[0][1], self.equipment1.name)
        self.assertEqual(self.equipment1.complete_name, self.equipment1.name)
        self.assertEqual(self.equipment1.display_name, self.equipment1.name)

        self.assertEqual(
            self.equipment1_1.name_get()[0][1], equipment1_1_complete_name)
        self.assertEqual(
            self.equipment1_1.complete_name, equipment1_1_complete_name)
        self.assertEqual(
            self.equipment1_1.display_name, equipment1_1_complete_name)
