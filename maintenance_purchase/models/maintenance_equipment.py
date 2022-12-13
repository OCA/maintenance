# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    purchase_id = fields.Many2one(
        comodel_name="purchase.order",
        related="purchase_line_id.order_id",
        string="Purchase",
        readonly=True,
    )
    purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        readonly=True,
    )
