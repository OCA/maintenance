# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    maintenance_result = fields.Selection(
        selection=[
            ("none", "No Result"),
            ("passed", "Passed"),
            ("failed", "Failed"),
        ],
        default="none",
        copy=False,
        tracking=True,
    )
    source_request_id = fields.Many2one(
        comodel_name="maintenance.request",
        string="Source Request",
        copy=False,
        readonly=True,
        help="Failed request this follow-up request was created from.",
    )
    followup_request_ids = fields.One2many(
        comodel_name="maintenance.request",
        inverse_name="source_request_id",
        string="Follow-up Requests",
    )

    def action_create_followup_request(self):
        self.ensure_one()
        followup = self.env["maintenance.request"].create(
            {
                "name": _("Follow-up of %s", self.name),
                "equipment_id": self.equipment_id.id,
                "maintenance_type": "corrective",
                "source_request_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "maintenance.request",
            "res_id": followup.id,
            "view_mode": "form",
            "target": "current",
        }
