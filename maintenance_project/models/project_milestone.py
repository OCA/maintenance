# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    maintenance_request_ids = fields.One2many(
        comodel_name="maintenance.request",
        inverse_name="milestone_id",
        string="Maintenance Requests",
    )

    maintenance_request_count = fields.Integer(
        compute="_compute_maintenance_request_count",
        string="Maintenance Requests Count",
    )

    @api.depends("maintenance_request_ids")
    def _compute_maintenance_request_count(self):
        for milestone in self:
            milestone.maintenance_request_count = len(milestone.maintenance_request_ids)

    def action_view_maintenance_request(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance_project.action_view_maintenance_request_for_milestone"
        )
        action["context"] = {
            "default_project_id": self.project_id.id,
            "default_milestone_id": self.id,
        }
        if self.maintenance_request_count == 1:
            action["view_mode"] = "form"
            action["res_id"] = self.maintenance_request_ids.id
            if "views" in action:
                action["views"] = [
                    (view_id, view_type)
                    for view_id, view_type in action["views"]
                    if view_type == "form"
                ]
        return action
