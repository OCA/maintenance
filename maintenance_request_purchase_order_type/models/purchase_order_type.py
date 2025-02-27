# Copyright 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    use_maintenance_request = fields.Boolean(
        string="Use in Maintenance Requests", default=False
    )
