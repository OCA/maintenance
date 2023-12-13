# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipmentMeter(models.Model):

    _name = "maintenance.equipment.meter"
    _description = "Meter log for an equipment"
    _order = "date desc"

    name = fields.Char(compute="_compute_meter_name", store=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    value = fields.Float("Meter Value", group_operator="max")
    equipment_id = fields.Many2one("maintenance.equipment", required=True)
    meter_unit_id = fields.Many2one(
        related="equipment_id.meter_unit_id", string="Unit", readonly=True
    )

    @api.depends("equipment_id.name", "date")
    def _compute_meter_name(self):
        for record in self:
            record.name = "%s / %s" % (record.equipment_id.name, str(record.date))
