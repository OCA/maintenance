# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceLocation(models.Model):
    _inherit = "maintenance.location"

    owner_id = fields.Many2one("res.users")
