# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    tag_ids = fields.Many2many(
        "maintenance.request.tag",
        "request_tag_rel",
        "request_id",
        "tag_id",
        string="Tags",
    )
