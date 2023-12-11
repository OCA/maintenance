# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    location_id = fields.Many2one("maintenance.location")

    @api.onchange("equipment_id")
    def _onchange_equipment_id(self):
        for record in self:
            if record.equipment_id and record.equipment_id.location_id:
                record.location_id = record.equipment_id.location_id
