# Copyright 2019 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    user_id = fields.Many2one(comodel_name="res.users", string="Team Leader")
    description = fields.Text()
