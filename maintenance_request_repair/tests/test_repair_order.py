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

        self.request1 = self.env["maintenance.request"].create(
            {
                "name": "Request 1",
                "repair_order_id": self.repair_order.id,
            }
        )
        self.request2 = self.env["maintenance.request"].create(
            {
                "name": "Request 2",
                "repair_order_id": self.repair_order.id,
            }
        )

        self.equipment = self.env["maintenance.equipment"].create(
            {"name": "Equipment 1"}
        )
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})

    def test_compute_maintenance_request_count(self):
        self.repair_order.write(
            {"maintenance_request_ids": [(4, self.request1.id), (4, self.request2.id)]}
        )
        self.repair_order._compute_maintenance_request_count()
        assert self.repair_order.maintenance_request_count == 2

    def test_action_view_maintenance_request(self):

        self.result = self.repair_order.with_user(
            self.env.user
        ).action_view_maintenance_request()
        self.repair_order.write(
            {"maintenance_request_ids": [(4, self.request1.id), (4, self.request2.id)]}
        )
        self.assertEqual(
            self.result["context"], {"default_repair_order_id": self.repair_order.id}
        )
        self.maintenance_request_ids = self.repair_order.mapped(
            "maintenance_request_ids"
        )
        with self.subTest("Choose the view_mode accordingly"):

            with self.subTest(
                "Check maintenance_request_ids > 1 OR not self.maintenance_request_ids"
            ):
                self.assertTrue(
                    len(self.repair_order.maintenance_request_ids) > 1
                    or not self.repair_order.maintenance_request_ids
                )
                self.result["domain"] = "[('id','in',%s)]" % (
                    self.maintenance_request_ids.ids
                )
                self.assertEqual(
                    self.result["domain"],
                    "[('id','in',%s)]" % (self.maintenance_request_ids.ids),
                )

            self.repair_order.write(
                {"maintenance_request_ids": [(6, 0, self.request1.id)]}
            )
            self.maintenance_request_ids = self.repair_order.maintenance_request_ids
            self.result = self.repair_order.action_view_maintenance_request()

            with self.subTest("Check maintenance_request_ids == 1"):

                self.assertEqual(len(self.maintenance_request_ids), 1)
                res = self.env.ref("maintenance.hr_equipment_request_view_form", False)
                form_view = [(res and res.id or False, "form")]

                with self.subTest("Check view in result"):

                    self.assertIn("views", self.result)
                    self.result["views"] = form_view + [
                        (state, view)
                        for state, view in self.result["views"]
                        if view != "form"
                    ]
                    self.assertEqual(
                        self.result["views"],
                        (
                            form_view
                            + [
                                (state, view)
                                for state, view in self.result["views"]
                                if view != "form"
                            ]
                        ),
                    )

                self.assertNotEqual(self.result["views"], form_view)
                del self.result["views"]

                self.repair_order.write(
                    {"maintenance_request_ids": [(2, self.request1.id)]}
                )
                self.maintenance_request_ids = self.repair_order.maintenance_request_ids

                with self.subTest("Check view not in result"):
                    self.assertNotIn("views", self.result)
                    self.result["views"] = form_view
                    self.assertEqual(self.result["views"], form_view)

                self.result["res_id"] = self.maintenance_request_ids.id
                self.assertEqual(self.result["res_id"], self.maintenance_request_ids.id)

    def test_create_repair_order(self):
        self.repair_order = self.env["repair.order"].create(
            {
                "partner_id": self.partner.id,
                "product_id": self.product.id,
            }
        )
        self.repair_order.name = "Repair Order Test 2"
        self.assertEqual(self.repair_order.name, "Repair Order Test 2")
        self.assertEqual(self.repair_order.partner_id, self.partner)
        self.assertEqual(self.repair_order.product_id, self.product)

    def test_simple_view_maintenance_request(self):
        self.repair_order = self.env["repair.order"].create(
            {
                "name": "Repair Order Test",
                "partner_id": self.partner.id,
                "product_id": self.product.id,
            }
        )
        self.maintenance_request = self.env["maintenance.request"].create(
            {
                "name": "Maintenance Request Test",
                "repair_order_id": self.repair_order.id,
            }
        )
        self.action = self.repair_order.action_view_maintenance_request()
        self.assertEqual(self.action["type"], "ir.actions.act_window")
        self.assertEqual(self.action["res_model"], "maintenance.request")
        self.assertEqual(
            self.action["view_mode"], "kanban,tree,form,pivot,graph,calendar"
        )
        self.assertEqual(self.action["target"], "current")
        self.assertEqual(self.action["res_id"], self.maintenance_request.id)

    def test_maintenance_request_count(self):
        self.env["maintenance.request"].create(
            {
                "name": "Maintenance Request Test",
                "repair_order_id": self.repair_order.id,
            }
        )
        self.assertEqual(self.repair_order.maintenance_request_count, 3)

    def test_clear_maintenance_request(self):
        self.action = self.repair_order.action_view_maintenance_request()
        self.assertEqual(self.action["type"], "ir.actions.act_window")
        self.assertEqual(self.action["name"], "Maintenance Requests")
        self.assertEqual(
            self.action["context"], {"default_repair_order_id": self.repair_order.id}
        )
        self.assertEqual(self.action["views"][0][1], "kanban")
        self.assertEqual(self.action["views"][1][1], "tree")
        self.assertEqual(self.action["views"][2][1], "form")
        self.assertEqual(self.action["views"][3][1], "pivot")
        self.assertEqual(self.action["views"][4][1], "graph")
        self.assertEqual(self.action["views"][5][1], "calendar")
        self.assertEqual(len(self.action["views"]), 6)
