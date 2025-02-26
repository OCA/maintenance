# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    purchase_order_ids = fields.Many2many(
        "purchase.order",
        "maintenance_purchase_order",
        "maintenance_request_id",
        "purchase_order_id",
        groups="purchase.group_purchase_user",
        string="Purchase Orders",
        copy=False,
    )
    purchases_count = fields.Integer(
        compute="_compute_purchases_count",
        store=True,
        groups="purchase.group_purchase_user",
    )

    @api.depends("purchase_order_ids")
    def _compute_purchases_count(self):
        for record in self:
            record.purchases_count = len(record.purchase_order_ids.ids)
