# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as test_common


class TestMaintenanceStock(test_common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.maintenance_warehouse = self.env["stock.warehouse"].create({
            "name": "Test warehouse",
            "code": "TEST",
        })

        self.product1 = self.env["product.product"].create({
            "default_code": "TESTOPROD",
            "name": "Test prod",
            "type": "product",
            "uom_id": self.env.ref("uom.product_uom_unit").id,
            "uom_po_id": self.env.ref("uom.product_uom_unit").id,
        })

        self.equipment_1 = self.env["maintenance.equipment"].create({
            "name": 'Test equipment',
            "allow_consumptions": True,
            "default_consumption_warehouse_id": self.maintenance_warehouse.id,
        })
        self.request_1 = self.env["maintenance.request"].create({
            'name': 'Test request',
            "user_id": self.env.ref("base.user_demo").id,
            "owner_user_id": self.env.ref("base.user_admin").id,
            "equipment_id": self.equipment_1.id,
            "stage_id": self.env.ref("maintenance.stage_1").id,
            "maintenance_team_id":
                self.env.ref("maintenance.equipment_team_maintenance").id,
        })

    def test_warehouse(self):
        self.assertTrue(self.maintenance_warehouse.wh_cons_loc_id)

        self.assertTrue(self.maintenance_warehouse.cons_type_id)
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.code, "outgoing")
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.default_location_src_id,
            self.maintenance_warehouse.lot_stock_id)
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.default_location_dest_id,
            self.maintenance_warehouse.wh_cons_loc_id)
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.barcode,
            self.maintenance_warehouse.code.replace(" ", "").upper() + "-CONS")
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.sequence_id.prefix,
            self.maintenance_warehouse.code + '/CONS/')
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.return_picking_type_id,
            self.maintenance_warehouse.in_type_id)

    def test_equipment(self):
        self.assertTrue(self.equipment_1.default_consumption_warehouse_id)
        self.equipment_1.allow_consumptions = False
        self.equipment_1._onchange_allow_consumptions()
        self.assertFalse(self.equipment_1.default_consumption_warehouse_id)

        action1 = self.equipment_1.action_view_stock_picking_ids()
        self.assertEqual(action1["domain"][0][2], self.equipment_1.id)
        self.assertTrue(action1["context"]["show_maintenance_request_id"])

        action2 = self.equipment_1.action_view_stock_move_ids()
        self.assertEqual(action2["domain"][0][2], self.equipment_1.id)

        action3 = self.equipment_1.action_view_stock_move_line_ids()
        self.assertEqual(action3["domain"][0][2], self.equipment_1.id)
        self.assertFalse(
            action3["context"]["search_default_groupby_location_dest_id"])

    def test_request(self):
        action1 = self.request_1.action_view_stock_picking_ids()
        self.assertEqual(action1["domain"][0][2], self.request_1.id)
        self.assertEqual(
            action1["context"]["default_picking_type_id"],
            self.request_1.default_consumption_warehouse_id.cons_type_id.id)
        self.assertEqual(
            action1["context"]["default_maintenance_request_id"],
            self.request_1.id)

        action2 = self.request_1.action_view_stock_move_ids()
        self.assertEqual(action2["domain"][0][2], self.request_1.id)

        action3 = self.request_1.action_view_stock_move_line_ids()
        self.assertEqual(action3["domain"][0][2], self.request_1.id)
        self.assertFalse(
            action3["context"]["search_default_groupby_location_dest_id"])

    def test_picking(self):
        self.assertEqual(len(self.request_1.stock_picking_ids), 0)
        self.assertEqual(len(self.equipment_1.stock_picking_ids), 0)

        qty_done = 5.0
        picking = self.env["stock.picking"].create({
            "maintenance_request_id": self.request_1.id,
            "picking_type_id": self.maintenance_warehouse.cons_type_id.id,
            "location_id": self.maintenance_warehouse.lot_stock_id.id,
            "location_dest_id": self.maintenance_warehouse.wh_cons_loc_id.id,
            "move_lines": [(0, 0, {
                "name": "Test move",
                "product_id": self.product1.id,
                "product_uom": self.env.ref("uom.product_uom_unit").id,
                "product_uom_qty": 5.0,
                "picking_type_id": self.maintenance_warehouse.cons_type_id.id,
                "location_id": self.maintenance_warehouse.lot_stock_id.id,
                "location_dest_id":
                    self.maintenance_warehouse.wh_cons_loc_id.id,
                "move_line_ids": [(0, 0, {
                    "product_id": self.product1.id,
                    "product_uom_id": self.env.ref("uom.product_uom_unit").id,
                    "qty_done": qty_done,
                    "location_id": self.maintenance_warehouse.lot_stock_id.id,
                    "location_dest_id":
                        self.maintenance_warehouse.wh_cons_loc_id.id,
                })]
            })]
        })

        self.assertEqual(len(self.request_1.stock_picking_ids), 1)
        self.assertEqual(len(self.equipment_1.stock_picking_ids), 1)

        stock_quant_obj = self.env["stock.quant"]
        domain_from = [
            ("product_id", "=", self.product1.id),
            ("location_id", "=", self.maintenance_warehouse.lot_stock_id.id)
        ]
        domain_to = [
            ("product_id", "=", self.product1.id),
            ("location_id", "=", self.maintenance_warehouse.wh_cons_loc_id.id)
        ]
        self.assertEqual(stock_quant_obj.search(domain_from).quantity, 0)
        self.assertEqual(stock_quant_obj.search(domain_to).quantity, 0)

        picking.action_confirm()
        picking.action_done()

        self.assertEqual(
            stock_quant_obj.search(domain_from).quantity, -qty_done)
        self.assertEqual(
            stock_quant_obj.search(domain_to).quantity, qty_done)
