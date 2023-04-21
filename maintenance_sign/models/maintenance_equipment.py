# Copyright 2023 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    sign_request_ids = fields.One2many(
        comodel_name="sign.request",
        inverse_name="maintenance_equipment_id",
        string="Sign Requests",
    )
    sign_request_count = fields.Integer(
        string="Sign request count",
        compute="_compute_sign_request_count",
        compute_sudo=True,
        store=True,
    )

    @api.depends("sign_request_ids")
    def _compute_sign_request_count(self):
        request_data = self.env["sign.request"].read_group(
            [("maintenance_equipment_id", "in", self.ids)],
            ["maintenance_equipment_id"],
            ["maintenance_equipment_id"],
        )
        mapped_data = {
            x["maintenance_equipment_id"][0]: x["maintenance_equipment_id_count"]
            for x in request_data
        }
        for item in self:
            item.sign_request_count = mapped_data.get(item.id, 0)

    def action_view_sign_requests(self):
        self.ensure_one()
        action = self.env.ref("sign_oca.sign_request_all_action")
        result = action.read()[0]
        result["domain"] = [("id", "in", self.sign_request_ids.ids)]
        ctx = dict(self.env.context)
        ctx.update(
            {
                "default_maintenance_equipment_id": self.id,
                "search_default_maintenance_equipment_id": self.id,
            }
        )
        result["context"] = ctx
        return result

    def action_maintenance_equipment_sign_request(self):
        action = self.env.ref("sign_oca.wizard_sign_request_action")
        result = action.read()[0]
        ctx = dict(self.env.context)
        result["context"] = ctx
        return result
