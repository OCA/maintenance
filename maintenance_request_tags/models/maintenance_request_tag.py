# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models


class MaintenanceRequestTag(models.Model):
    _name = "maintenance.request.tag"
    _description = "Maintenance Request Tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Request Tag", required=True)
    color = fields.Integer(default=lambda self: self._get_default_color())
    request_ids = fields.Many2many(
        "maintenance.request",
        "request_tag_rel",
        "tag_id",
        "request_id",
        string="Maintenance Requests",
    )

    _name_uniq = models.Constraint("unique (name)", "Tag name already exists !")
