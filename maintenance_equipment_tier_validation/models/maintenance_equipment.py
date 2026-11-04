# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _name = "maintenance.equipment"
    _inherit = ["maintenance.equipment", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["confirmed"]
    _cancel_state = "cancel"

    _tier_validation_manual_config = False

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        copy=False,
        tracking=True,
    )

    def action_validate_equipment(self):
        # Only draft is under tier validation; confirming from cancel would skip it.
        self.filtered(lambda rec: rec.state == "draft").write({"state": "confirmed"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    @api.model
    def _get_after_validation_exceptions(self):
        # Cancel and archive must work; cancelling drops the reviews anyway.
        return super()._get_after_validation_exceptions() + ["state", "active"]
