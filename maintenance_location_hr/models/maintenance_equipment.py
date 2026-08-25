# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    equipment_assign_to = fields.Selection(
        selection_add=[("location", "Location")],
        ondelete={"location": lambda r: r.write({"equipment_assign_to": "other"})},
    )

    @api.depends("employee_id", "department_id", "equipment_assign_to", "location_id")
    def _compute_owner(self):
        location_equipments = self.filtered(
            lambda r: r.equipment_assign_to == "location"
        )
        for equipment in location_equipments:
            equipment.owner_user_id = equipment.location_id.owner_id or self.env.user
        return super(MaintenanceEquipment, self - location_equipments)._compute_owner()
