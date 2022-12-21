# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrTimesheetSwitch(models.TransientModel):
    _inherit = "hr.timesheet.switch"

    @api.model
    def _closest_suggestion(self):
        """Allow to search the best suggestion by maintenance.request."""
        result = super()._closest_suggestion()
        try:
            if not result and self.env.context["active_model"] == "maintenance.request":
                return self.env["account.analytic.line"].search(
                    [
                        ("user_id", "=", self.env.user.id),
                        ("maintenance_request_id", "=", self.env.context["active_id"]),
                    ],
                    order="date_time DESC",
                    limit=1,
                )
        except KeyError:
            # If I don't know where's the user, I don't know what to suggest
            pass
        return result
