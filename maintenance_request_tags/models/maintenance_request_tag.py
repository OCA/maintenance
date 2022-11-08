# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from random import randint

from odoo import api, fields, models


class MaintenanceRequestTag(models.Model):

    _name = "maintenance.request.tag"
    _description = "Maintenance Request Tag"

    name = fields.Char(string="Request Tag", required=True)
    color = fields.Integer(string="Color Index (0-15)", default=randint(1, 15))
    request_ids = fields.Many2many(
        "maintenance.request",
        "request_tag_rel",
        "tag_id",
        "request_id",
        string="Maintenance Requests",
    )

    selectable_team_ids = fields.Many2many(
        "maintenance.team", string="Selectable Teams"
    )

    selectable_team_count = fields.Integer(
        compute="_compute_selectable_team_count", store=True, readonly=True
    )

    @api.depends("selectable_team_ids")
    def _compute_selectable_team_count(self):
        for record in self:
            record.selectable_team_count = len(record.selectable_team_ids)

    _sql_constraints = [("name_uniq", "unique (name)", "Tag name already exists !")]
