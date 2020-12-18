# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestMaintenanceEquipment(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestMaintenanceEquipment, cls).setUpClass()
        cls.user_admin = cls.env.ref('base.user_root')
        cls.Equipment = cls.env['maintenance.equipment']
        cls.Category = cls.env['maintenance.equipment.category']

        cls.equipment_category = cls.Category.create({
            'name': 'AF Category',
        })

        cls.equipment1 = cls.Equipment.create({
            'name': 'Equipment with AF Category',
            'category_id': cls.equipment_category.id,
        })

    def test_maintenance_equipment_always_fold(self):
        self.assertEqual(
            self.equipment_category.fold,
            False,
            'Equipment category with equipments maybe not fold'
        )

        self.equipment_category.always_fold = True
        self.assertEqual(
            self.equipment_category.fold,
            True,
            'Equipment categ with equipments but always fold check maybe fold'
        )
