# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models


class MaintenanceEquipmentTag(models.Model):

    _name = "maintenance.equipment.tag"
    _description = "Maintenance Equipment Tag"

    def get_default_color_value(self):
        return randint(1, 15)

    name = fields.Char(string="Equipment Tag", required=True)
    color = fields.Integer(
        string="Color Index (0-15)", default=lambda self: self.get_default_color_value()
    )
    equipment_ids = fields.Many2many(
        "maintenance.equipment",
        "equipment_tag_rel",
        "tag_id",
        "equipment_id",
        string="Equipment",
    )

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists !"),
    ]
