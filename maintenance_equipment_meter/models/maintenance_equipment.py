# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    has_meter = fields.Boolean()
    meter_unit_id = fields.Many2one("uom.uom")
    current_meter = fields.Float(
        compute="_compute_meter",
        inverse="_inverse_meter",
        string="Last meter",
        compute_sudo=True,
    )
    current_meter_show = fields.Float(related="current_meter", readonly=True)

    @api.depends()
    def _compute_meter(self):
        ManintenanceEquipmentMeter = self.env["maintenance.equipment.meter"]
        for record in self:
            meter = ManintenanceEquipmentMeter.search(
                [("equipment_id", "=", record.id)], limit=1, order="value desc"
            )
            if meter:
                record.current_meter = meter.value
            else:
                record.current_meter = 0

    def _inverse_meter(self):
        for record in self:
            if record.current_meter and record.has_meter:
                date = fields.Date.context_today(record)
                data = {
                    "value": record.current_meter,
                    "date": date,
                    "equipment_id": record.id,
                }
                self.env["maintenance.equipment.meter"].sudo().create(data)
