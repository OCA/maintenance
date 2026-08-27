# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    availability_state = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        compute="_compute_availability",
        store=True,
        readonly=True,
        string="Availability",
    )
    latest_maintenance_result_request_id = fields.Many2one(
        comodel_name="maintenance.request",
        compute="_compute_availability",
        store=True,
        readonly=True,
        string="Latest Result Request",
    )
    latest_maintenance_result_date = fields.Date(
        compute="_compute_availability",
        store=True,
        readonly=True,
        string="Latest Result Date",
    )

    @api.depends(
        "maintenance_ids.close_date",
        "maintenance_ids.request_date",
        "maintenance_ids.stage_id.done",
        "maintenance_ids.maintenance_result",
        "maintenance_ids.archive",
    )
    def _compute_availability(self):
        requests = (
            self.env["maintenance.request"]
            .sudo()
            .search(
                [
                    ("equipment_id", "in", self.ids),
                    ("stage_id.done", "=", True),
                    ("maintenance_result", "in", ("passed", "failed")),
                    ("archive", "=", False),
                ],
                order="equipment_id, close_date desc, request_date desc, id desc",
            )
        )
        latest_by_equipment = {}
        for request in requests:
            latest_by_equipment.setdefault(request.equipment_id.id, request)
        for equipment in self:
            request = latest_by_equipment.get(equipment.id)
            equipment.latest_maintenance_result_request_id = request
            equipment.latest_maintenance_result_date = (
                request.close_date or request.request_date if request else False
            )
            if not request:
                equipment.availability_state = "unknown"
            elif request.maintenance_result == "passed":
                equipment.availability_state = "available"
            else:
                equipment.availability_state = "unavailable"
