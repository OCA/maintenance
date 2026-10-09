# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request",
        related="picking_id.maintenance_request_id",
    )
    maintenance_equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        related="picking_id.maintenance_equipment_id",
    )
