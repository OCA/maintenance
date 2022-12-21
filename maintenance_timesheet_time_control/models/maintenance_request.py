# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MaintenanceRequest(models.Model):
    _name = "maintenance.request"
    _inherit = ["maintenance.request", "hr.timesheet.time_control.mixin"]

    @api.model
    def _relation_with_timesheet_line(self):
        return "maintenance_request_id"

    @api.depends(
        "project_id.allow_timesheets",
        "timesheet_ids.employee_id",
        "timesheet_ids.unit_amount",
    )
    def _compute_show_time_control(self):
        result = super()._compute_show_time_control()
        self.filtered(lambda x: not x.project_id.allow_timesheets).update(
            {"show_time_control": False}
        )
        return result

    def button_start_work(self):
        result = super().button_start_work()
        result["context"].update(
            {
                "default_project_id": self.project_id.id,
                "default_task_id": self.task_id.id,
            }
        )
        return result
