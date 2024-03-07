# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestMaintenanceProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Equipment = cls.env["maintenance.equipment"]
        cls.EquipmentCategory = cls.env["maintenance.equipment.category"]
        cls.MaintenanceEquipmentCategory = cls.env["maintenance.equipment.category"]
        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.PurchaseOrderLine = cls.env["purchase.order.line"]
        cls.ProductCategory = cls.env["product.category"]
        cls.ProductProduct = cls.env["product.product"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.ResPartner = cls.env["res.partner"]

        cls.partner = cls.ResPartner.create(
            {
                "name": "partner",
            }
        )
        uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.maintenance_equipment_category1 = cls.MaintenanceEquipmentCategory.create(
            {"name": "My Maintenance Equipment Category 1"}
        )
        cls.maintenance_equipment_category2 = cls.MaintenanceEquipmentCategory.create(
            {"name": "My Maintenance Equipment Category 2"}
        )
        cls.product_category01 = cls.ProductCategory.create(
            {
                "name": "My Product Category 1",
                "equipment_category_ids": [
                    Command.set(
                        [
                            cls.maintenance_equipment_category1.id,
                            cls.maintenance_equipment_category2.id,
                        ]
                    )
                ],
            }
        )
        cls.product_category02 = cls.ProductCategory.create(
            {
                "name": "My Product Category 2",
                "equipment_category_ids": [
                    Command.set([cls.maintenance_equipment_category2.id])
                ],
            }
        )
        cls.product_order_maintenance = cls.ProductProduct.create(
            {
                "name": "My Product",
                "standard_price": 235.0,
                "list_price": 280.0,
                "type": "consu",
                "uom_id": uom_unit.id,
                "uom_po_id": uom_unit.id,
                "purchase_method": "purchase",
                "default_code": "PROD_ORDER",
                "taxes_id": False,
                "maintenance_ok": True,
                "categ_id": cls.product_category01.id,
            }
        )
        cls.product_order_no_maintenance = cls.ProductProduct.create(
            {
                "name": "My Product",
                "standard_price": 235.0,
                "list_price": 280.0,
                "type": "consu",
                "uom_id": uom_unit.id,
                "uom_po_id": uom_unit.id,
                "purchase_method": "purchase",
                "default_code": "PROD_ORDER",
                "taxes_id": False,
                "categ_id": cls.product_category02.id,
            }
        )
        cls.purchase_order = cls.PurchaseOrder.with_context(
            tracking_disable=True
        ).create(
            {
                "partner_id": cls.partner.id,
            }
        )
        PurchaseOrderLine = cls.PurchaseOrderLine.with_context(tracking_disable=True)
        cls.purchase_line_order01 = PurchaseOrderLine.create(
            {
                "name": cls.product_order_maintenance.name,
                "product_id": cls.product_order_maintenance.id,
                "product_qty": 10.0,
                "product_uom": cls.product_order_maintenance.uom_id.id,
                "price_unit": cls.product_order_maintenance.list_price,
                "order_id": cls.purchase_order.id,
                "taxes_id": False,
            }
        )
        cls.purchase_line_order02 = PurchaseOrderLine.create(
            {
                "name": cls.product_order_no_maintenance.name,
                "product_id": cls.product_order_no_maintenance.id,
                "product_qty": 10.0,
                "product_uom": cls.product_order_no_maintenance.uom_id.id,
                "price_unit": cls.product_order_no_maintenance.list_price,
                "order_id": cls.purchase_order.id,
                "taxes_id": False,
            }
        )

    def test_equipment_count(self):
        self.purchase_order.button_approve()
        self.assertEqual(self.purchase_order.equipment_count, 10)
        self.assertEqual(self.purchase_line_order01.equipment_count, 10)
        self.assertEqual(self.purchase_line_order02.equipment_count, 0)
        self.purchase_order.button_draft()
        self.purchase_line_order01.product_qty = 1
        self.purchase_order.button_approve()
        self.assertEqual(self.purchase_order.equipment_count, 10)
        self.purchase_order.button_draft()
        self.purchase_line_order01.equipment_ids.unlink()
        self.purchase_order.button_approve()
        self.assertEqual(self.purchase_order.equipment_count, 1)

    def test_unlink_purchase_oder(self):
        self.purchase_order.button_approve()
        equipments = self.purchase_order.order_line.equipment_ids
        self.assertEqual(equipments.purchase_id, self.purchase_order)
        self.assertEqual(equipments.purchase_line_id, self.purchase_line_order01)
        self.purchase_order.button_cancel()
        self.assertEqual(equipments.purchase_id, self.purchase_order)
        self.assertEqual(equipments.purchase_line_id, self.purchase_line_order01)
        self.purchase_order.unlink()
        self.assertFalse(equipments.purchase_id)
        self.assertFalse(equipments.purchase_line_id)

    def test_equipment_category_id(self):
        self.assertEqual(
            self.purchase_line_order01.equipment_category_id,
            self.maintenance_equipment_category1,
        )
        self.assertFalse(self.purchase_line_order02.equipment_category_id)
        self.product_order_no_maintenance.product_tmpl_id.maintenance_ok = True
        self.assertFalse(self.purchase_line_order02.equipment_category_id)
        self.purchase_line_order02.product_id = self.product_order_maintenance
        self.purchase_line_order02.product_id = self.product_order_no_maintenance
        self.assertEqual(
            self.purchase_line_order02.equipment_category_id,
            self.maintenance_equipment_category2,
        )
        self.purchase_line_order01.equipment_ids.unlink()
        self.purchase_line_order01.equipment_category_id = False
        self.purchase_order.button_approve()
        self.assertEqual(
            self.purchase_line_order01.equipment_category_id,
            self.maintenance_equipment_category1,
        )
        self.purchase_line_order01.equipment_ids.unlink()
        self.purchase_line_order01.equipment_category_id = False
        product_category_withouth_equipement_category = self.ProductCategory.create(
            {
                "name": "My Product Category 2",
            }
        )
        self.purchase_line_order01.product_id.product_tmpl_id.categ_id = (
            product_category_withouth_equipement_category.id
        )
        self.purchase_order.button_approve()
        self.assertTrue(self.purchase_line_order01.equipment_category_id)
        self.assertNotEqual(
            self.purchase_line_order01.equipment_category_id,
            self.maintenance_equipment_category1,
        )

    def test_account_move_line(self):
        self.purchase_order.button_approve()
        self.purchase_order.action_create_invoice()
        self.assertEqual(
            self.purchase_order.order_line.equipment_ids,
            self.purchase_order.invoice_ids.line_ids.equipment_ids,
        )

    def test_action_view_equipments(self):
        action = self.purchase_order.action_view_equipments()
        self.assertEqual(action, {"type": "ir.actions.act_window_close"})
        self.purchase_line_order01.product_qty = 1
        self.purchase_order.button_approve()
        view = self.env.ref("maintenance.hr_equipment_view_form", False)
        action = self.purchase_order.action_view_equipments()
        self.assertEqual(action["views"], [(view and view.id or False, "form")])
        self.assertEqual(
            action["res_id"], self.purchase_line_order01.equipment_ids[0:].id
        )
        self.purchase_order.button_draft()
        self.purchase_line_order01.equipment_ids.unlink()
        self.purchase_line_order01.product_qty = 2
        self.purchase_order.button_approve()
        action = self.purchase_order.action_view_equipments()
        self.assertEqual(
            action["domain"], [("purchase_id", "=", self.purchase_order.id)]
        )
