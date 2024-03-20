# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlan(models.Model):

    _inherit = "maintenance.plan"

    location_id = fields.Many2one("maintenance.location")
