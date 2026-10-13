# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"
    _rec_names_search = ["code"]

    code = fields.Char(readonly=True, copy=False, default="/")

    @api.model_create_multi
    def create(self, vals_list):
        pending_vals = [vals for vals in vals_list if vals.get("code", "/") == "/"]
        if pending_vals:
            team_ids = {
                vals["maintenance_team_id"]
                for vals in pending_vals
                if vals.get("maintenance_team_id")
            }
            # Browse all the teams at once so their sequence is read in a
            # single query instead of one query per request being created.
            teams = self.env["maintenance.team"].browse(team_ids)
            team_sequences = {team.id: team.sequence_id for team in teams}
            default_sequence = self.env.ref(
                "maintenance_request_sequence.seq_maintenance_request_auto"
            )
            for vals in pending_vals:
                sequence = (
                    team_sequences.get(vals.get("maintenance_team_id"))
                    or default_sequence
                )
                vals["code"] = sequence.next_by_id()
        return super().create(vals_list)
