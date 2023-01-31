# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    sequence_code = fields.Char(default="IN")
