# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceInspectionLine(models.Model):

    _name = "maintenance.inspection.line"
    _description = "Maintenance Inspection Line"

    request_id = fields.Many2one(
        "maintenance.request", required=True, ondelete="cascade"
    )
    item_id = fields.Many2one("maintenance.inspection.item", required=True)
    instruction = fields.Text(related="item_id.instruction")
    result = fields.Selection(
        [("todo", "Todo"), ("success", "Success"), ("failure", "Failure")],
        "Result",
        default="todo",
        readonly=True,
        required=True,
        copy=False,
    )
    result_description = fields.Char()
    inspection_closed_at = fields.Datetime(related="request_id.inspection_closed_at")

    def action_success(self):
        self.write({"result": "success"})

    def action_failure(self):
        self.write({"result": "failure"})
