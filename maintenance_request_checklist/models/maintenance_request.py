# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    checklist_ids = fields.One2many(
        comodel_name="maintenance.request.checklist.line",
        inverse_name="request_id",
        string="Checklist",
    )
    checklist_total = fields.Integer(
        string="Total Steps", compute="_compute_checklist_progress", store=True
    )
    checklist_done = fields.Integer(
        string="Steps Done", compute="_compute_checklist_progress", store=True
    )

    @api.depends("checklist_ids.is_done")
    def _compute_checklist_progress(self):
        for rec in self:
            lines = rec.checklist_ids
            rec.checklist_total = len(lines)
            rec.checklist_done = len(lines.filtered("is_done"))
