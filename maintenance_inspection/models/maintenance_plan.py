# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlan(models.Model):

    _inherit = "maintenance.plan"

    inspection_item_ids = fields.Many2many("maintenance.inspection.item")
