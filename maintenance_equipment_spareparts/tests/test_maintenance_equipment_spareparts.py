# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestMaintenanceEquipmentSpareparts(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Equipment = cls.env["maintenance.equipment"]
        cls.Sparepart = cls.env["maintenance.equipment.sparepart"]
        cls.Request = cls.env["maintenance.request"]
        cls.Product = cls.env["product.product"]
        cls.Warehouse = cls.env["stock.warehouse"]

        # Create test product
        cls.product = cls.Product.create(
            {
                "name": "Test Spare Part",
                "purchase_ok": True,
                "type": "consu",
                "is_storable": True,
            }
        )

        # Create test equipment
        cls.equipment = cls.Equipment.create(
            {
                "name": "Test Equipment",
            }
        )

        # Create warehouse for stock operations
        cls.warehouse = cls.env.ref("stock.warehouse0")

    def test_create_sparepart(self):
        """Test creating a spare part."""
        sparepart = self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 5.0,
            }
        )
        self.assertEqual(sparepart.equipment_id, self.equipment)
        self.assertEqual(sparepart.product_id, self.product)
        self.assertEqual(sparepart.installed_qty, 2.0)
        self.assertEqual(sparepart.spare_qty, 5.0)

    def test_duplicate_sparepart_validation(self):
        """Test that duplicate spare parts are not allowed."""
        self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 5.0,
            }
        )
        with self.assertRaises(ValidationError):
            self.Sparepart.create(
                {
                    "equipment_id": self.equipment.id,
                    "product_id": self.product.id,
                    "installed_qty": 1.0,
                    "spare_qty": 3.0,
                }
            )

    def test_negative_quantity_validation(self):
        """Test that negative quantities are not allowed."""
        with self.assertRaises(ValidationError):
            self.Sparepart.create(
                {
                    "equipment_id": self.equipment.id,
                    "product_id": self.product.id,
                    "installed_qty": -1.0,
                    "spare_qty": 5.0,
                }
            )

    def test_needs_reorder_computation(self):
        """Test needs_reorder computed field."""
        sparepart = self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 5.0,
            }
        )
        # Initially should need reorder if no stock
        sparepart.invalidate_recordset(["needs_reorder"])
        self.assertTrue(sparepart.needs_reorder)

    def test_sparepart_count(self):
        """Test sparepart_count computation."""
        initial_count = self.equipment.sparepart_count
        self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 5.0,
            }
        )
        self.equipment.invalidate_recordset(["sparepart_count"])
        self.assertEqual(self.equipment.sparepart_count, initial_count + 1)

    def test_purchase_request_product_restriction(self):
        """Test that purchase request line validates product is sparepart."""
        # Create sparepart
        self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 5.0,
            }
        )
        # Create purchase request with equipment
        purchase_request = self.env["purchase.request"].create(
            {
                "requested_by": self.env.user.id,
                "equipment_id": self.equipment.id,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
            }
        )
        # Should allow sparepart product
        line = self.env["purchase.request.line"].create(
            {
                "request_id": purchase_request.id,
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "product_qty": 1.0,
            }
        )
        self.assertEqual(line.product_id, self.product)

    def test_purchase_request_product_restriction_fail(self):
        """Test that purchase request blocks non-sparepart products."""
        # Create another product that is NOT a sparepart
        other_product = self.Product.create(
            {
                "name": "Other Product",
                "purchase_ok": True,
                "type": "consu",
                "is_storable": True,
            }
        )
        # Create purchase request with equipment
        purchase_request = self.env["purchase.request"].create(
            {
                "requested_by": self.env.user.id,
                "equipment_id": self.equipment.id,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
            }
        )
        # Should NOT allow non-sparepart product
        with self.assertRaises(ValidationError):
            self.env["purchase.request.line"].create(
                {
                    "request_id": purchase_request.id,
                    "product_id": other_product.id,
                    "product_uom_id": other_product.uom_id.id,
                    "product_qty": 1.0,
                }
            )

    def test_action_create_purchase_request(self):
        """Test action to create purchase request for low stock."""
        # Create sparepart with low stock
        self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 2.0,
                "spare_qty": 10.0,  # High spare qty, so needs reorder
            }
        )
        result = self.equipment.action_create_purchase_request()
        # Should return action with purchase request
        self.assertIn("res_id", result)
        purchase_request = self.env["purchase.request"].browse(result["res_id"])
        self.assertEqual(purchase_request.equipment_id, self.equipment)
        self.assertTrue(purchase_request.line_ids)

    def test_consume_spareparts_creates_purchase_request_link(self):
        """Purchase request created from consume wizard links to request."""
        sparepart = self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 1.0,
                "spare_qty": 2.0,
            }
        )
        request = self.Request.create(
            {
                "name": "REQ-TEST-001",
                "equipment_id": self.equipment.id,
            }
        )
        wizard = self.env["maintenance.request.consume.spareparts"].create(
            {
                "request_id": request.id,
                "line_ids": [
                    (0, 0, {"sparepart_id": sparepart.id, "requested_qty": 1.0})
                ],
            }
        )
        wizard.action_consume()

        purchase_request = self.env["purchase.request"].search(
            [("maintenance_request_id", "=", request.id)], limit=1
        )
        self.assertTrue(purchase_request)
        self.assertEqual(purchase_request.maintenance_request_id, request)
        self.assertEqual(purchase_request.equipment_id, self.equipment)
        request.invalidate_recordset(["purchase_request_ids", "purchase_request_count"])
        self.assertEqual(request.purchase_request_count, 1)

    def test_consume_spareparts_negative_quantity(self):
        """Negative quantities should raise an error."""
        sparepart = self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 1.0,
                "spare_qty": 2.0,
            }
        )
        request = self.Request.create(
            {
                "name": "REQ-TEST-NEG",
                "equipment_id": self.equipment.id,
            }
        )
        wizard = self.env["maintenance.request.consume.spareparts"].create(
            {
                "request_id": request.id,
                "line_ids": [(0, 0, {"sparepart_id": sparepart.id})],
            }
        )
        wizard.line_ids[0].requested_qty = -1.0
        with self.assertRaises(UserError):
            wizard.action_consume()

    def test_purchase_request_equipment_must_match_request(self):
        """Purchase request equipment must match maintenance request equipment."""
        other_equipment = self.Equipment.create({"name": "Other Equipment"})
        request = self.Request.create(
            {
                "name": "REQ-TEST-002",
                "equipment_id": self.equipment.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["purchase.request"].create(
                {
                    "requested_by": self.env.user.id,
                    "equipment_id": other_equipment.id,
                    "maintenance_request_id": request.id,
                    "picking_type_id": self.env.ref("stock.picking_type_in").id,
                }
            )

    def test_existing_purchase_request_is_linked(self):
        """Existing purchase request is linked to the maintenance request."""
        sparepart = self.Sparepart.create(
            {
                "equipment_id": self.equipment.id,
                "product_id": self.product.id,
                "installed_qty": 1.0,
                "spare_qty": 2.0,
            }
        )
        request = self.Request.create(
            {
                "name": "REQ-TEST-003",
                "equipment_id": self.equipment.id,
            }
        )
        purchase_request = self.env["purchase.request"].create(
            {
                "requested_by": self.env.user.id,
                "company_id": request.company_id.id,
                "origin": request.name,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
            }
        )
        request._create_purchase_request_for_sparepart(sparepart, 1.0)
        purchase_request.invalidate_recordset(["maintenance_request_id"])
        self.assertEqual(purchase_request.maintenance_request_id, request)
