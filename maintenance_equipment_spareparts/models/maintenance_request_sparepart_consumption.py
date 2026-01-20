# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MaintenanceRequestSparepartConsumption(models.Model):
    _name = "maintenance.request.sparepart.consumption"
    _description = "Maintenance Request Spare Part Consumption"
    _rec_name = "product_id"
    _order = "create_date desc"

    request_id = fields.Many2one(
        comodel_name="maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sparepart_id = fields.Many2one(
        comodel_name="maintenance.equipment.sparepart",
        string="Spare Part",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        related="sparepart_id.product_id",
        store=True,
        readonly=True,
    )
    consumed_qty = fields.Float(
        string="Consumed Quantity",
        required=True,
    )
    stock_picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Stock Picking",
        help="Stock picking created when part was consumed from stock",
    )
    purchase_request_id = fields.Many2one(
        comodel_name="purchase.request",
        string="Purchase Request",
        help="Purchase request created when part was not in stock",
    )
    purchase_request_line_id = fields.Many2one(
        comodel_name="purchase.request.line",
        string="Purchase Request Line",
        help="Purchase request line created when part was not in stock",
    )
    state = fields.Selection(
        selection=[
            ("consumed", "Consumed from Stock"),
            ("requested", "Purchase Request Created"),
            ("pending", "Pending"),
        ],
        default="pending",
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="request_id.company_id",
        store=True,
        readonly=True,
    )
