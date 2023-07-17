# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceTeam(models.Model):

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"
    _inherit = "maintenance.team"

    parent_id = fields.Many2one("maintenance.team", ondelete="restrict")
    parent_path = fields.Char(index=True, unaccent=False)

    request_ids = fields.Many2many(
        "maintenance.request",
        compute="_compute_request_ids",
    )

    todo_request_ids = fields.One2many(compute="_compute_new_todo_requests")
    todo_request_count = fields.Integer(compute="_compute_new_todo_requests")
    todo_request_count_date = fields.Integer(compute="_compute_new_todo_requests")
    todo_request_count_high_priority = fields.Integer(
        compute="_compute_new_todo_requests"
    )
    todo_request_count_block = fields.Integer(compute="_compute_new_todo_requests")
    todo_request_count_unscheduled = fields.Integer(
        compute="_compute_new_todo_requests"
    )

    def _compute_request_ids(self):
        for record in self:
            record.request_ids = self.env["maintenance.request"].search(
                record._get_request_domains()
            )

    def _get_request_domains(self):
        return [("maintenance_team_id", "child_of", self.id)]

    @api.depends()
    def _compute_new_todo_requests(self):
        """This is the only way to remove the api depends fields. This is necessary
        because request_ids is now a computed field
        """
        self._compute_todo_requests()

    def _compute_todo_requests(self):
        """This function improves the computation and simplifies the data"""
        request_obj = self.env["maintenance.request"]
        for record in self:
            domain = record._get_request_domains() + [("stage_id.done", "=", False)]
            record.todo_request_ids = request_obj.search(domain)
            record.todo_request_count = request_obj.search_count(domain)
            record.todo_request_count_date = request_obj.search_count(
                domain + [("schedule_date", "!=", False)]
            )
            record.todo_request_count_high_priority = request_obj.search_count(
                domain + [("priority", "=", "3")]
            )
            record.todo_request_count_block = request_obj.search_count(
                domain + [("kanban_state", "=", "blocked")]
            )
            record.todo_request_count_unscheduled = request_obj.search_count(
                domain + [("schedule_date", "=", False)]
            )
