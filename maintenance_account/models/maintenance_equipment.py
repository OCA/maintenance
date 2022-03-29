# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    move_id = fields.Many2one(
        comodel_name="account.move",
        related="move_line_id.move_id",
        string="Move",
        readonly=True,
    )
    move_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Move line",
        readonly=True,
    )
