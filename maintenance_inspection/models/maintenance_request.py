# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    has_inspection = fields.Boolean()
    inspection_line_ids = fields.One2many(
        "maintenance.inspection.line", inverse_name="request_id"
    )
    inspection_closed_at = fields.Datetime(readonly=True, copy=False)
    inspection_closed_by = fields.Many2one("res.users", readonly=True, copy=False)

    def set_inspection(self):
        self.write({"has_inspection": True})

    def finish_inspection(self):
        self.write(
            {
                "inspection_closed_at": fields.Datetime.now(),
                "inspection_closed_by": self.env.user.id,
            }
        )
