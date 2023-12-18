# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceInspectionItem(models.Model):

    _name = "maintenance.inspection.item"
    _description = "Item of evaluation"

    name = fields.Char(required=True)
    instruction = fields.Text()
    active = fields.Boolean(default=True)
