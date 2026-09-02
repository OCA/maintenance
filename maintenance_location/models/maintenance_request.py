# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    location_id = fields.Many2one(
        "maintenance.location",
        compute="_compute_location_id",
        store=True,
        readonly=False,
    )

    @api.depends(
        "equipment_id", "equipment_id.location_id", "stage_id", "stage_id.done"
    )
    def _compute_location_id(self):
        for record in self:
            if record.equipment_id and record.equipment_id.location_id:
                if record.stage_id and record.stage_id.done:
                    # if the request is done, we want keep existing location
                    pass
                else:
                    record.location_id = record.equipment_id.location_id
            else:
                record.location_id = False
