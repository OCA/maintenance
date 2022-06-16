# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EquipmentChecklist(models.Model):
    _name = "equipment.checklist"
    _description = "Equipment Checklist"

    name = fields.Char("Checklist Name", required=True)
    description = fields.Text("Description", required=True)
    instruction = fields.Html("Instructions")
    active = fields.Boolean("Active", default=True)


class MaintenanceChecklist(models.Model):
    _name = "maintenance.checklist"
    _description = "Maintenance Checklist"

    name = fields.Char(
        string="Name", required=True, related="checklist_id.name"
    )
    description_checklist = fields.Text(
        string="Description",
        required=True,
        related="checklist_id.description",
    )
    equipment_id = fields.Many2one(
        "maintenance.equipment",
        "Equipment",
        related="request_id.equipment_id",
    )
    request_id = fields.Many2one(
        "maintenance.request", "Maintenance Request"
    )
    checklist_id = fields.Many2one("equipment.checklist", "Checklist")
    state = fields.Selection(
        [
            ("new", "Not started yet"),
            ("process", "In Progress"),
            ("block", "On Hold"),
            ("done", "Completed"),
        ],
        string="Status",
        default="new",
    )
    instruction = fields.Html(
        "Instructions", related="checklist_id.instruction"
    )
    reason = fields.Text("Work Description")

    def confirm_checklist(self):
        self.write({"state": "process"})

    def mark_as_done(self):
        self.write({"state": "done"})

    def mark_as_hold(self):
        self.write({"state": "block"})


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    checklist_ids = fields.One2many(
        "maintenance.checklist", "request_id", "Checklists"
    )
    total_checklist = fields.Float(
        "Total Checklist", compute="_compute_checklists"
    )
    completed_checklist = fields.Integer(
        "Completed Checklist", compute="_compute_checklists"
    )
    inprogress_checklist = fields.Integer(
        "In-progress Checklist", compute="_compute_checklists"
    )
    onhold_checklist = fields.Integer(
        "On-Hold Checklist", compute="_compute_checklists"
    )

    def _compute_checklists(self):
        for maintenance in self:
            maintenance.total_checklist = len(
                maintenance.checklist_ids
            )
            inprogress_checklist = 0
            onhold_checklist = 0
            completed_checklist = 0
            for checklist in maintenance.checklist_ids:
                if checklist.state == "process":
                    inprogress_checklist += 1
                if checklist.state == "block":
                    onhold_checklist += 1
                if checklist.state == "done":
                    completed_checklist += 1
            maintenance.completed_checklist = completed_checklist
            maintenance.inprogress_checklist = inprogress_checklist
            maintenance.onhold_checklist = onhold_checklist
