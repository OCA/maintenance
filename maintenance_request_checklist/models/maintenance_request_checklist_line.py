# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequestChecklistLine(models.Model):
    _name = "maintenance.request.checklist.line"
    _description = "Maintenance Request Checklist Line"
    _order = "sequence, id"

    request_id = fields.Many2one(
        comodel_name="maintenance.request",
        string="Maintenance Request",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Step", required=True)
    is_done = fields.Boolean(string="Done")
    done_by = fields.Many2one(
        comodel_name="res.users",
        readonly=True,
    )
    done_date = fields.Datetime(string="Done On", readonly=True)
    meter_value = fields.Integer(string="Meter Reading")
    notes = fields.Char()

    def write(self, vals):
        if "is_done" in vals:
            if vals["is_done"]:
                vals.setdefault("done_by", self.env.uid)
                vals.setdefault("done_date", fields.Datetime.now())
            else:
                vals["done_by"] = False
                vals["done_date"] = False
        return super().write(vals)
