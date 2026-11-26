# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class MaintenanceEquipmentTag(models.Model):
    _name = "maintenance.equipment.tag"
    _description = "Maintenance Equipment Tag"

    name = fields.Char(string="Equipment Tag", required=True)
    color = fields.Integer()
    equipment_ids = fields.Many2many(
        "maintenance.equipment",
        "equipment_tag_rel",
        "tag_id",
        "equipment_id",
    )

    _name_uniq = models.Constraint("unique (name)", "Tag name already exists !")
