# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    maintenance_request_ids = fields.Many2many(
        "maintenance.request",
        "maintenance_purchase_order",
        "purchase_order_id",
        "maintenance_request_id",
        string="Maintenance Requests",
        copy=False,
    )

    maintenance_requests_count = fields.Integer(
        compute="_compute_maintenance_requests_count", store=True
    )

    @api.depends("maintenance_request_ids")
    def _compute_maintenance_requests_count(self):
        for record in self:
            record.maintenance_requests_count = len(record.maintenance_request_ids.ids)

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
