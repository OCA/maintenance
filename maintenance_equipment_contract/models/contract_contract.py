# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    equipment_ids = fields.Many2many("maintenance.equipment", string="Equipments")
    equipment_count = fields.Integer(compute="_compute_equipment_count")

    @api.depends("equipment_ids")
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)

    def action_show_maintenance_requests(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance.hr_equipment_request_action"
        )
        action["domain"] = self._action_show_maintenance_requests_domain()
        return action

    def _action_show_maintenance_requests_domain(self):
        return [("equipment_id", "in", self.equipment_ids.ids)]
