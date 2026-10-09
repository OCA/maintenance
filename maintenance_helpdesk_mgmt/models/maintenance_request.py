# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    helpdesk_ticket_ids = fields.Many2many(
        "helpdesk.ticket",
        "maintenance_helpdesk_ticket",
        "maintenance_request_id",
        "helpdesk_ticket_id",
        string="Helpdesk Tickets",
        copy=False,
    )
    helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")

    def _compute_helpdesk_ticket_count(self):
        group_data = self.env["helpdesk.ticket"]._read_group(
            domain=[("maintenance_request_ids", "in", self.ids)],
            groupby=["maintenance_request_ids"],
            aggregates=["__count"],
        )
        mapped_data = {
            maintenance_request.id: count for (maintenance_request, count) in group_data
        }
        for maintenance_request in self:
            maintenance_request.helpdesk_ticket_count = mapped_data.get(
                maintenance_request.id, 0
            )

    def action_view_helpdesk_tickets(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "helpdesk_mgmt.helpdesk_ticket_action"
        )
        if len(self.helpdesk_ticket_ids) > 1:
            action["domain"] = [("id", "in", self.helpdesk_ticket_ids.ids)]
        elif self.helpdesk_ticket_ids:
            action["views"] = [(False, "form")]
            action["res_id"] = self.helpdesk_ticket_ids.id
        action["context"] = {}
        return action
