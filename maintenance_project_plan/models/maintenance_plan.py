# Copyright 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"

    project_id = fields.Many2one(comodel_name="project.project", ondelete="restrict")
    task_id = fields.Many2one(
        comodel_name="project.task",
        compute="_compute_task_id",
        store="True",
        readonly=False,
    )

    @api.depends("project_id")
    def _compute_task_id(self):
        for plan in self:
            plan.task_id = False
