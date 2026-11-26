# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form

from .common import TestMaintenanceProductBase


class TestMaintenanceProduct(TestMaintenanceProductBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env["maintenance.equipment.category"].create(
            {"name": "test-maintenance-equipment-category"}
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {"name": "test-maintenance-equipment"}
        )

    def test_maintenance_equipment_category(self):
        category_form = Form(self.category)
        category_form.product_category_id = self.product_category
        self.assertEqual(category_form.name, "test-product-category")

    def test_maintenance_equipment(self):
        equipment_form = Form(self.equipment)
        equipment_form.product_id = self.product
        self.assertEqual(equipment_form.name, "test-product")
        self.assertEqual(equipment_form.cost, 10)
        self.assertEqual(equipment_form.partner_id, self.partner)
