# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceLocation(models.Model):

    _name = "maintenance.location"
    _description = "Maintenance Location"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"
    _rec_name = "complete_name"
    _order = "complete_name,id"

    name = fields.Char(required=True)
    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )

    partner_id = fields.Many2one("res.partner")

    parent_id = fields.Many2one(
        "maintenance.location",
        "Parent Location",
        index=True,
        ondelete="cascade",
    )
    child_id = fields.One2many(
        "maintenance.location", "parent_id", "Child Locations"
    )
    parent_left = fields.Integer("Left Parent", index=1)
    parent_right = fields.Integer("Right Parent", index=1)

    sequence = fields.Integer(string="Sequence", default=10)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for location in self:
            if location.parent_id:
                location.complete_name = "%s / %s" % (
                    location.parent_id.complete_name,
                    location.name,
                )
            else:
                location.complete_name = location.name

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                _("Error ! You cannot create recursive Locations.")
            )
        return True
