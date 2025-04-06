# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestMaintenanceCategory(TransactionCase):
    def setUp(self):
        super().setUp()
        self.category_1 = self.env["maintenance.equipment.category"].create(
            {"name": "C1"}
        )
        self.category_2 = self.env["maintenance.equipment.category"].create(
            {"name": "C2", "parent_id": self.category_1.id}
        )

    def test_maintenance_category(self):
        self.assertEqual(self.category_2.complete_name, "C1 / C2")
        with self.assertRaises(UserError):
            self.category_1.write({"parent_id": self.category_2.id})
