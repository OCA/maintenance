# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class MaintenanceChecklistCreateTimesheet(models.TransientModel):
    _name = "maintenance.checklist.create.timesheet"
    _description = "Create Timesheet from maintenance request"

    _sql_constraints = [
        (
            "time_positive",
            "CHECK(time_spent > 0)",
            "The timesheet's time must be positive",
        )
    ]

    time_spent = fields.Float("Time", digits=(16, 2))
    description = fields.Char("Description")
    checklist_id = fields.Many2one(
        "maintenance.checklist",
        "Checklist",
        required=True,
        default=lambda self: self.env.context.get("active_id", None),
    )

    def save_timesheet(self):
        if not self.checklist_id.request_id.project_id:
            raise ValidationError(
                _("You must specify the project in the maintenance request!")
            )
        task_id = self.checklist_id.request_id.task_id
        values = {
            "maintenance_request_id": self.checklist_id.request_id.id,
            "task_id": task_id and task_id.id or False,
            "project_id": self.checklist_id.request_id.project_id.id,
            "date": fields.Date.context_today(self),
            "name": self.description,
            "user_id": self.env.uid,
            "unit_amount": self.time_spent,
        }
        self.checklist_id.user_timer_id.unlink()
        self.env["account.analytic.line"].create(values)
        return self.checklist_id.mark_as_done()
