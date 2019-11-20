# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    active = fields.Boolean(default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Team Leader",
    )
    description = fields.Text()
