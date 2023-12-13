# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"
    has_meter = fields.Boolean(related="equipment_id.has_meter")
    meter_unit_id = fields.Many2one("uom.uom", related="equipment_id.meter_unit_id")
    meter_id = fields.Many2one("maintenance.equipment.meter")
    current_meter = fields.Float(
        compute="_compute_meter",
        inverse="_inverse_meter",
        string="Last meter",
        compute_sudo=True,
        store=True,
    )

    @api.depends("meter_id.value")
    def _compute_meter(self):
        for record in self:
            record.current_meter = record.meter_id.value or 0.0

    def _inverse_meter(self):
        for rec in self:
            if not rec.current_meter and self.meter_id:
                raise UserError(
                    _("Emptying the odometer value of an equipment is not allowed.")
                )
            if not rec.current_meter:
                continue
            meter = (
                self.env["maintenance.equipment.meter"]
                .sudo()
                .create(
                    {
                        "value": rec.current_meter,
                        "date": fields.Date.context_today(rec),
                        "equipment_id": rec.equipment_id.id,
                    }
                )
            )
            self.meter_id = meter

    @api.onchange("equipment_id")
    def onchange_equipment_id(self):
        result = super().onchange_equipment_id()
        if self.meter_id and self.equipment_id != self.meter_id.sudo().equipment_id:
            self.meter_id = False
        return result
