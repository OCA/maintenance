# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request",
        index=True,
    )
    maintenance_equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        related="maintenance_request_id.equipment_id",
        store=True,
    )
