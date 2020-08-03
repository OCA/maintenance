# © 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    maintenance_request_id = fields.Many2one(
        comodel_name='maintenance.request')

    @api.onchange('maintenance_request_id')
    def onchange_maintenance_request_id(self):
        if self.maintenance_request_id and not self.project_id:
            self.project_id = self.maintenance_request_id.project_id
            self.task_id = self.maintenance_request_id.task_id

    @api.model
    def create(self, values):
        if values.get('maintenance_request_id'):
            self._check_request_done(values.get('maintenance_request_id'))
        return super().create(values)

    @api.multi
    def write(self, values):
        for timesheet in self:
            if timesheet.maintenance_request_id or values.get(
                    'maintenance_request_id', False):
                timesheet._check_request_done(
                    timesheet.maintenance_request_id.id
                    if timesheet.maintenance_request_id
                    else values['maintenance_request_id'])
        return super().write(values)

    def unlink(self):
        for timesheet in self.filtered(lambda x: x.maintenance_request_id):
            self._check_request_done(timesheet.maintenance_request_id.id)
        super().unlink()

    def _check_request_done(self, request_id):
        """
        Editing a timesheet related to a finished request is forbidden.
        """
        if self.env['maintenance.request'].browse(request_id).stage_id.done:
            raise ValidationError(_('Cannot save or delete a timesheet for '
                                    'a maintenance request already done'))
