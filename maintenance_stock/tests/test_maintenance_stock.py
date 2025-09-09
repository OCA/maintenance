# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import Form, common


class TestMaintenanceStock(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.maintenance_warehouse = self.env["stock.warehouse"].create(
            {
                "name": "Test warehouse",
                "code": "TEST",
            }
        )

        self.product1 = self.env["product.product"].create(
            {
                "default_code": "TESTOPROD",
                "name": "Test prod",
                "type": "consu",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "uom_po_id": self.env.ref("uom.product_uom_unit").id,
                "is_storable": True,
            }
        )

        self.equipment_1 = self.env["maintenance.equipment"].create(
            {
                "name": "Test equipment",
                "allow_consumptions": True,
                "default_consumption_warehouse_id": self.maintenance_warehouse.id,
            }
        )
        self.request_1 = self.env["maintenance.request"].create(
            {
                "name": "Test request",
                "user_id": self.env.ref("base.user_demo").id,
                "owner_user_id": self.env.ref("base.user_admin").id,
                "equipment_id": self.equipment_1.id,
                "stage_id": self.env.ref("maintenance.stage_1").id,
                "maintenance_team_id": self.env.ref(
                    "maintenance.equipment_team_maintenance"
                ).id,
            }
        )

    def test_warehouse(self):
        self.assertTrue(self.maintenance_warehouse.wh_cons_loc_id)

        self.assertTrue(self.maintenance_warehouse.cons_type_id)
        self.assertEqual(self.maintenance_warehouse.cons_type_id.code, "outgoing")
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.default_location_src_id,
            self.maintenance_warehouse.lot_stock_id,
        )
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.default_location_dest_id,
            self.maintenance_warehouse.wh_cons_loc_id,
        )
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.barcode,
            self.maintenance_warehouse.code.replace(" ", "").upper() + "-CONS",
        )
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.sequence_id.prefix,
            self.maintenance_warehouse.code + "/CONS/",
        )
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.return_picking_type_id,
            self.maintenance_warehouse.in_type_id,
        )

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
        self.assertFalse(action3["context"]["search_default_groupby_location_dest_id"])

    def test_request(self):
        action1 = self.request_1.action_view_stock_picking_ids()
        self.assertEqual(action1["domain"][0][2], self.request_1.id)
        self.assertEqual(
            action1["context"]["default_picking_type_id"],
            self.request_1.default_consumption_warehouse_id.cons_type_id.id,
        )
        self.assertEqual(
            action1["context"]["default_maintenance_request_id"], self.request_1.id
        )

        action2 = self.request_1.action_view_stock_move_ids()
        self.assertEqual(action2["domain"][0][2], self.request_1.id)

        action3 = self.request_1.action_view_stock_move_line_ids()
        self.assertEqual(action3["domain"][0][2], self.request_1.id)
        self.assertFalse(action3["context"]["search_default_groupby_location_dest_id"])

    def test_picking(self):
        self.assertEqual(len(self.request_1.stock_picking_ids), 0)
        location_id = self.maintenance_warehouse.lot_stock_id
        picking_type_id = self.maintenance_warehouse.cons_type_id
        self.env["stock.quant"].create(
            {
                "product_id": self.product1.id,
                "location_id": location_id.id,
                "quantity": 5,
            }
        )
        picking_form = Form(self.env["stock.picking"])
        picking_form.picking_type_id = picking_type_id
        picking_form.location_id = location_id
        with picking_form.move_ids_without_package.new() as move:
            move.product_id = self.product1
            move.product_uom_qty = 5.0
        picking = picking_form.save()
        picking.write({"maintenance_request_id": self.request_1.id})
        self.assertEqual(len(self.request_1.stock_picking_ids), 1)
        stock_quant_obj = self.env["stock.quant"]
        domain_from = [
            ("product_id", "=", self.product1.id),
            ("location_id", "=", self.maintenance_warehouse.lot_stock_id.id),
        ]
        domain_to = [
            ("product_id", "=", self.product1.id),
            ("location_id", "=", self.maintenance_warehouse.wh_cons_loc_id.id),
        ]
        self.assertEqual(stock_quant_obj.search(domain_from).quantity, 5)
        self.assertEqual(stock_quant_obj.search(domain_to).quantity, 0)

        picking.action_confirm()
        picking.action_assign()
        picking.move_line_ids.write({"quantity": 5.0, "picked": True})
        picking.button_validate()
        self.assertEqual(stock_quant_obj.search(domain_from).quantity, 0)
        self.assertEqual(stock_quant_obj.search(domain_to).quantity, 5)

    def test_update_name_and_code(self):
        """Test that _update_name_and_code updates the sequence prefix only."""
        new_code = "UPDT"
        self.maintenance_warehouse.code = new_code
        self.maintenance_warehouse._update_name_and_code()
        expected_prefix = new_code + "/CONS/"
        self.assertEqual(
            self.maintenance_warehouse.cons_type_id.sequence_id.prefix,
            expected_prefix,
        )
