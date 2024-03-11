# © 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    maintenance_request_id = fields.Many2one(comodel_name="maintenance.request")

    @api.onchange("maintenance_request_id")
    def onchange_maintenance_request_id(self):
        if self.maintenance_request_id and not self.project_id:
            self.project_id = self.maintenance_request_id.project_id
            self.task_id = self.maintenance_request_id.task_id

    @api.model_create_multi
    def create(self, vals_list):
        maintenance_request_ids = [
            vals.get("maintenance_request_id")
            for vals in vals_list
            if vals.get("maintenance_request_id")
        ]
        self._check_request_done(maintenance_request_ids)
        return super().create(vals_list)

    def write(self, values):
        current_request = self.maintenance_request_id
        new_request_id = values.get("maintenance_request_id", False)
        if current_request:
            self._check_request_done(current_request.id)
        if new_request_id:
            self._check_request_done(new_request_id)
        return super().write(values)

    def unlink(self):
        self._check_request_done(
            self.filtered(lambda x: x.maintenance_request_id).maintenance_request_id.ids
        )
        return super().unlink()

    def _check_request_done(self, request_id: int | list[int]):
        """
        Editing a timesheet related to a finished request is forbidden.
        """
        request_ids = [request_id] if isinstance(request_id, int) else request_id
        if any(
            self.env["maintenance.request"].browse(request_ids).stage_id.mapped("done")
        ):
            raise ValidationError(
                _(
                    "Cannot save or delete a timesheet for "
                    "a maintenance request already done"
                )
            )
