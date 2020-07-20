# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    tag_ids = fields.Many2many(
        "maintenance.equipment.tag",
        "equipment_tag_rel",
        "equipment_id",
        "tag_id",
        string="Tags",
    )
