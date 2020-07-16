# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

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

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        # Make a search with default criteria
        names1 = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        # Make the other search
        names2 = []
        if name:
            domain = [("code", "=ilike", name + "%")]
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
