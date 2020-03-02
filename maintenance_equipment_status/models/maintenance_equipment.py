# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    status_id = fields.Many2one(
        string="Status",
        comodel_name="maintenance.equipment.status",
        track_visibility="onchange",
    )
    status_name = fields.Char(
        string="Status name", related="status_id.name", store=True
    )
