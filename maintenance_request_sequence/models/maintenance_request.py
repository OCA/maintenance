# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"
    _rec_names_search = ["code"]

    code = fields.Char(readonly=True, copy=False, default="/")

    @api.model
    def create(self, vals):
        if vals.get("code", "/") == "/":
            team_id = vals.get("maintenance_team_id")
            sequence = self.env["maintenance.team"].browse(
                team_id
            ).sequence_id or self.env.ref(
                "maintenance_request_sequence.seq_maintenance_request_auto"
            )
            vals["code"] = sequence.next_by_id()
        return super().create(vals)
