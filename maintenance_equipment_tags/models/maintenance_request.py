# Copyright 2022 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    tag_ids = fields.Many2many(
        comodel_name="maintenance.equipment.tag",
        relation="request_tag_rel",
        column1="request_id",
        column2="tag_id",
        string="Tags",
    )

