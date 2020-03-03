# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestMaintenanceEquipmentStatus(common.TransactionCase):
    def setUp(self):
        super(TestMaintenanceEquipmentStatus, self).setUp()
        self.Equipment = self.env["maintenance.equipment"]
        self.EquipmentStatus = self.env["maintenance.equipment.status"]
        self.Category = self.env["maintenance.equipment.category"]
        self.Template = self.env["mail.template"]
        self.equipment_category = self.Category.create({"name": "Equipment Category"})

        self.equipment1 = self.Equipment.create(
            {"name": "Equipment 1", "category_id": self.equipment_category.id}
        )

        self.equipment2 = self.Equipment.create(
            {"name": "Equipment 2", "category_id": self.equipment_category.id}
        )
        self.equipment_status = self.EquipmentStatus.create(
            {"name": "State 1", "category_ids": [(6, 0, self.equipment_category.ids)]}
        )

    def test_01(self):
        status = self.EquipmentStatus.search([])
        self.assertEqual(status, self.equipment_status)
        self.equipment1.status_id = self.equipment_status
        self.assertEqual(self.equipment1.status_name, "State 1")
