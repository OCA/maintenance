# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MaintenanceEquipmentCategory(models.Model):

    _inherit = "maintenance.equipment.category"

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"
    _rec_name = "complete_name"
    _order = "parent_id"

    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )

    parent_id = fields.Many2one(
        "maintenance.equipment.category",
        "Parent Category",
        index=True,
        ondelete="cascade",
    )
    child_id = fields.One2many(
        "maintenance.equipment.category", "parent_id", "Child Categories"
    )
    parent_path = fields.Char(index=True)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "{} / {}".format(
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("Error ! You cannot create recursive categories."))
        return True
