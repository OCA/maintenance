# Copyright 2025 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestMaintenancePurchaseStock(BaseCommon):
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
            }
        )
        cls.product_category02 = cls.ProductCategory.create(
            {
                "name": "My Product Category 2",
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
                "categ_id": cls.product_category01.id,
                "purchase_equipment_category_id": cls.maintenance_equipment_category1.id,  # noqa E501
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
        PurchaseOrderLine = cls.PurchaseOrderLine
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
        self.assertEqual(self.purchase_order.equipment_count, 0)
        self.assertEqual(self.purchase_line_order01.equipment_count, 0)
        self.assertEqual(self.purchase_line_order02.equipment_count, 0)
        self.purchase_order.picking_ids.button_validate()
        self.purchase_order.order_line._compute_qty_received()
        self.purchase_order.order_line._compute_equipment_count()
        self.purchase_order._compute_equipment_count()
        self.assertEqual(self.purchase_order.equipment_count, 10)
        self.assertEqual(self.purchase_line_order01.equipment_count, 10)
