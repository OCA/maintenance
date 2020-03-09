# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"

    project_id = fields.Many2one(comodel_name="project.project", ondelete="restrict")
    task_id = fields.Many2one(comodel_name="project.task")

    @api.onchange("project_id")
    def onchange_project_id(self):
        if self.project_id:
            if self.project_id != self.task_id.project_id:
                self.task_id = False
            return {"domain": {"task_id": [("project_id", "=", self.project_id.id)]}}
        else:
            self.task_id = False
            return {"domain": {"task_id": [("project_id", "=", False)]}}
