# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
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
    description = fields.Char()
    complete_name = fields.Char(
        compute="_compute_complete_name", store=True, recursive=True
    )

    partner_id = fields.Many2one("res.partner")

    parent_id = fields.Many2one(
        "maintenance.location",
        "Parent Location",
        index=True,
        ondelete="cascade",
    )
    child_id = fields.One2many("maintenance.location", "parent_id", "Child Locations")
    parent_path = fields.Char(index=True, unaccent=False)
    latitude = fields.Float(digits=(16, 5))
    longitude = fields.Float(digits=(16, 5))
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    equipment_ids = fields.One2many(
        "maintenance.equipment", "location_id", string="Equipments"
    )
    child_equipment_ids = fields.Many2many(
        comodel_name="maintenance.equipment",
        compute="_compute_child_equipment_ids",
        string="Child Equipments",
    )
    equipment_count = fields.Integer(compute="_compute_equipment_count")

    def _compute_child_equipment_ids(self):
        all_locations = self.env["maintenance.location"].search(
            [("id", "child_of", self.ids)]
        )
        all_equipments = self.env["maintenance.equipment"].search(
            [("location_id", "in", all_locations.ids)]
        )
        for location in self:
            descendant_locs = all_locations.filtered(
                lambda sub_loc, loc=location: sub_loc.parent_path
                and sub_loc.parent_path.startswith(loc.parent_path)
                and sub_loc.id != loc.id
            )
            location.child_equipment_ids = all_equipments.filtered(
                lambda eq, d_locs=descendant_locs: eq.location_id in d_locs
            )

    def _compute_equipment_count(self):
        all_locations = self.env["maintenance.location"].search(
            [("id", "child_of", self.ids)]
        )
        equip_data = self.env["maintenance.equipment"].read_group(
            domain=[("location_id", "in", all_locations.ids)],
            fields=["location_id"],
            groupby=["location_id"],
        )
        count_dict = {x["location_id"][0]: x["location_id_count"] for x in equip_data}
        for location in self:
            descendant_ids = all_locations.filtered(
                lambda sub_loc, loc=location: sub_loc.parent_path
                and sub_loc.parent_path.startswith(loc.parent_path)
            ).ids

            location.equipment_count = sum(
                count_dict.get(d_id, 0) for d_id in descendant_ids
            )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for location in self:
            if location.parent_id:
                location.complete_name = (
                    f"{location.parent_id.complete_name} / {location.name}"
                )
            else:
                location.complete_name = location.name

    @api.constrains("parent_id")
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("Error ! You cannot create recursive Locations."))
        return True
