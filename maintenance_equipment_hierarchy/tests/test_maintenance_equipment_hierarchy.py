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
