# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"

    parent_id = fields.Many2one(
        "maintenance.equipment",
        "Parent Equipment",
        index=True,
        ondelete="cascade",
        tracking=True,
    )
    child_ids = fields.One2many(
        "maintenance.equipment", "parent_id", "Child Equipments"
    )
    parent_left = fields.Integer("Left Parent", index=1)
    parent_right = fields.Integer("Right Parent", index=1)
    child_count = fields.Integer(
        compute="_compute_child_count", string="Number of child equipments"
    )
    display_name = fields.Char(compute="_compute_display_name")
    complete_name = fields.Char(
        compute="_compute_complete_name", store=True, recursive=True
    )
    parent_path = fields.Char(index=True)

    def name_get(self):
        return [(equipment.id, equipment.complete_name) for equipment in self]

    @api.depends("child_ids")
    def _compute_child_count(self):
        for equipment in self:
            equipment.child_count = len(equipment.child_ids)

    def _compute_display_name(self):
        for equipment in self:
            equipment.display_name = equipment.complete_name

    @api.depends("name", "parent_id.complete_name")  # recursive definition
    def _compute_complete_name(self):
        for equipment in self:
            if equipment.parent_id:
                parent_name = equipment.parent_id.complete_name
                equipment.complete_name = parent_name + " / " + equipment.name
            else:
                equipment.complete_name = equipment.name

    def preview_child_list(self):
        return {
            "name": _("Child equipment of %s") % self.name,
            "type": "ir.actions.act_window",
            "res_model": "maintenance.equipment",
            "res_id": self.id,
            "view_mode": "list,form",
            "context": {
                **self.env.context,
                "default_parent_id": self.id,
                "parent_id_editable": False,
            },
            "domain": [("parent_id", "=", self.id)],
        }
