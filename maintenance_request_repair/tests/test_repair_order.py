# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestRepairOrder(common.TransactionCase):
    def setUp(self):

        super(TestRepairOrder, self).setUp()

        self.product = self.env["product.product"].create(
            {
                "name": "Product Test",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "uom_po_id": self.env.ref("uom.product_uom_unit").id,
            }
        )

        self.location_id = self.env["stock.location"].create(
            {
                "name": "Test Location",
                "usage": "internal",
                "location_id": self.env.ref("stock.stock_location_stock").id,
            }
        )

        self.repair_order = self.env["repair.order"].create(
            {
                "name": "Test Repair Order",
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
                "location_id": self.location_id.id,
            }
        )

        self.request1 = self.env["maintenance.request"].create({"name": "Request 1"})
        self.request2 = self.env["maintenance.request"].create({"name": "Request 2"})
        self.repair_order.maintenance_request_ids += self.request1
        self.repair_order.maintenance_request_ids += self.request2

        self.equipment = self.env["maintenance.equipment"].create(
            {"name": "Equipment 1"}
        )

        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_compute_maintenance_request_count(self):

        self.repair_order._compute_maintenance_request_count()
        assert self.repair_order.maintenance_request_count == 2

    def test_action_view_maintenance_request(self):

        self.result = self.repair_order.action_view_maintenance_request()
        self.assertTrue(self.result)
        self.assertIn("context", self.result)
        self.assertIn("domain", self.result)
        self.assertIn("views", self.result)
        self.assertIn("res_id", self.result)
        self.assertEqual(
            self.result["context"], {"default_repair_order_id": self.repair_order.id}
        )
        self.maintenance_request_ids = self.repair_order.mapped(
            "maintenance_request_ids"
        )

        self.repair_order.maintenance_request_ids = False
        self.repair_order._compute_maintenance_request_count()
        self.action_result = self.repair_order.action_view_maintenance_request()
        self.assertTrue("domain" in self.action_result)

        self.repair_order.maintenance_request_ids = self.request1
        self.repair_order._compute_maintenance_request_count()
        self.action_result = self.repair_order.action_view_maintenance_request()
        self.assertTrue("views" in self.action_result)
        self.assertTrue("res_id" in self.action_result)
