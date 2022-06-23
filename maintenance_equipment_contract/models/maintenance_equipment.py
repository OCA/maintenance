# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    contract_ids = fields.Many2many("contract.contract", string="Contracts")
    contract_count = fields.Integer(
        compute="_compute_contract_count",
    )

    @api.depends("contract_ids")
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids.ids)

    def action_view_contracts(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "contract.action_customer_contract"
        )
        if len(self.contract_ids) > 1:
            action["domain"] = [("id", "in", self.contract_ids.ids)]
        elif self.contract_ids:
            action["views"] = [
                (self.env.ref("contract.contract_contract_form_view").id, "form")
            ]
            action["res_id"] = self.contract_ids.id
        action["context"] = {
            "default_equipment_ids": self.ids,
            "is_contract": 1,
            "search_default_not_finished": 1,
            "search_default_recurring_invoices": 1,
            "default_recurring_invoices": 1,
            "default_contract_type": "purchase",
        }
        return action
