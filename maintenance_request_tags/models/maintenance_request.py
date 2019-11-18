# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    selectable_tags_ids = fields.Many2many(
        "maintenance.request.tag",
        compute="_compute_selectable_tags_ids",
        readonly=True,
    )

    tag_ids = fields.Many2many(
        "maintenance.request.tag",
        "request_tag_rel",
        "request_id",
        "tag_id",
        string="Tags",
    )

    @api.depends("maintenance_team_id")
    def _compute_selectable_tags_ids(self):
        for record in self:
            record.selectable_tags_ids = [
                (6, 0, record.maintenance_team_id.selectable_tags_ids.ids)
            ]
            team_id = record.maintenance_team_id
            while team_id.parent_id:
                team_id = team_id.parent_id
                tags = [(4, tag) for tag in team_id.selectable_tags_ids.ids]
                record.selectable_tags_ids = tags
