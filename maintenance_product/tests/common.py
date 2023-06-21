# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestMaintenanceProductBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_category = cls.env["product.category"].create(
            {"name": "test-product-category"}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Mr Odoo"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "test-product",
                "categ_id": cls.product_category.id,
                "standard_price": 10,
                "maintenance_ok": True,
                "seller_ids": [(0, 0, {"partner_id": cls.partner.id})],
            }
        )
