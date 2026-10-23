# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    maintenance_request_ids = fields.Many2many(
        "maintenance.request",
        "maintenance_helpdesk_ticket",
        "helpdesk_ticket_id",
        "maintenance_request_id",
        string="Maintenance Requests",
        copy=False,
    )

    maintenance_request_count = fields.Integer(
        compute="_compute_maintenance_request_count"
    )

    def _compute_maintenance_request_count(self):
        group_data = self.env["maintenance.request"]._read_group(
            domain=[("helpdesk_ticket_ids", "in", self.ids)],
            groupby=["helpdesk_ticket_ids"],
            aggregates=["__count"],
        )
        mapped_data = {
            helpdesk_ticket.id: count for (helpdesk_ticket, count) in group_data
        }
        for helpdesk_ticket in self:
            helpdesk_ticket.maintenance_request_count = mapped_data.get(
                helpdesk_ticket.id, 0
            )

    def action_view_maintenance_request(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance.hr_equipment_request_action"
        )
        if len(self.maintenance_request_ids) > 1:
            action["domain"] = [("id", "in", self.maintenance_request_ids.ids)]
        elif self.maintenance_request_ids:
            action["views"] = [(False, "form")]
            action["res_id"] = self.maintenance_request_ids.id
        action["context"] = {}
        return action
