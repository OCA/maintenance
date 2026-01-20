# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MaintenanceEquipmentSparepart(models.Model):
    _name = "maintenance.equipment.sparepart"
    _description = "Maintenance Equipment Spare Part"
    _rec_name = "product_id"
    _order = "product_id"

    equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        string="Equipment",
        required=True,
        ondelete="cascade",
        index=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        domain="[('purchase_ok', '=', True)]",
    )
    installed_qty = fields.Float(
        string="Installed Quantity",
        required=True,
        default=0.0,
        help="Quantity of this part installed in the equipment",
    )
    spare_qty = fields.Float(
        string="Recommended Spare Quantity",
        required=True,
        default=0.0,
        help="Recommended quantity to keep in stock as spare",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="equipment_id.company_id",
        store=True,
        readonly=True,
    )
    active = fields.Boolean(default=True)
    available_qty = fields.Float(
        string="Available Quantity",
        compute="_compute_available_qty",
        help="Available quantity in stock",
    )
    needs_reorder = fields.Boolean(
        compute="_compute_needs_reorder",
        help="True if stock is below recommended spare quantity",
    )

    @api.depends("product_id", "product_id.qty_available")
    def _compute_available_qty(self):
        for record in self:
            if record.product_id:
                record.available_qty = record.product_id.qty_available
            else:
                record.available_qty = 0.0

    @api.depends("available_qty", "spare_qty")
    def _compute_needs_reorder(self):
        for record in self:
            record.needs_reorder = record.available_qty < record.spare_qty

    @api.constrains("installed_qty", "spare_qty")
    def _check_quantities(self):
        for record in self:
            if record.installed_qty < 0:
                raise ValidationError(
                    _("Installed quantity must be greater than or equal to 0.")
                )
            if record.spare_qty < 0:
                raise ValidationError(
                    _(
                        "Recommended spare quantity must be greater than or "
                        "equal to 0."
                    )
                )

    @api.constrains("equipment_id", "product_id")
    def _check_unique_product(self):
        for record in self:
            existing = self.search(
                [
                    ("equipment_id", "=", record.equipment_id.id),
                    ("product_id", "=", record.product_id.id),
                    ("id", "!=", record.id),
                    ("active", "=", True),
                ]
            )
            if existing:
                raise ValidationError(
                    _(
                        "Product %(product)s is already registered as a spare "
                        "part for equipment %(equipment)s."
                    )
                    % {
                        "product": record.product_id.display_name,
                        "equipment": record.equipment_id.display_name,
                    }
                )
