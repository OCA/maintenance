# Copyright 2023 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class SignRequest(models.Model):
    _inherit = "sign.request"

    maintenance_equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        compute="_compute_maintenance_equipment_id",
        string="Maintenance Equipment",
        readonly=True,
        store=True,
    )

    @api.onchange("record_ref")
    def _compute_maintenance_equipment_id(self):
        for item in self:
            if item.record_ref and item.record_ref._name == "maintenance.equipment":
                item.maintenance_equipment_id = item.record_ref
            else:
                item.maintenance_equipment_id = item.maintenance_equipment_id

    @api.onchange("maintenance_equipment_id")
    def _onchange_maintenance_equipment_id(self):
        if not self.partner_id and self.maintenance_equipment_id.owner_user_id:
            self.partner_id = self.maintenance_equipment_id.owner_user_id.partner_id
