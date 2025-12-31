# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    partner_id = fields.Many2one(
        "res.partner", compute="_compute_partner_id", store=True, readonly=False
    )

    @api.depends("equipment_id")
    def _compute_partner_id(self):
        for request in self:
            if request.equipment_id:
                request.partner_id = request.equipment_id.assigned_partner_id
