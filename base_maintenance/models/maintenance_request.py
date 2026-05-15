# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    team_member_ids = fields.Many2many(
        related="maintenance_team_id.member_ids",
        string="Team Members",
    )
