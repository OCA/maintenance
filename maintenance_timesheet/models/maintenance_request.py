# © 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    timesheet_ids = fields.One2many(
        string='Timesheets',
        comodel_name='account.analytic.line',
        inverse_name='maintenance_request_id')
    timesheet_total_hours = fields.Float(
        compute='_compute_timesheet_total_hours')

    def _add_followers(self):
        """
        Members of maintenance team are included as followers to automatically
        grant request visibility and timesheet permissions for this request
        """
        super()._add_followers()
        for request in self:
            partner_ids = \
                request.maintenance_team_id.member_ids.mapped('partner_id').ids
            request.message_subscribe(partner_ids=partner_ids)

    @api.depends('timesheet_ids.unit_amount')
    def _compute_timesheet_total_hours(self):
        for request in self:
            request.timesheet_total_hours = \
                sum(request.timesheet_ids.mapped('unit_amount'))

    def action_view_timesheet_ids(self):
        """
        Access to the current timesheets for this maintenance request
        The view will be restricted to the current request and only HR managers
        could create timesheets for every employee
        """
        self.ensure_one()
        action = self.env.ref(
            'maintenance_timesheet.timesheet_action_from_request').read()[0]
        action['domain'] = [('maintenance_request_id', '=', self.id)]
        action['context'] = {
            'default_project_id': self.project_id.id,
            'default_task_id': self.task_id.id,
            'default_maintenance_request_id': self.id,
            'readonly_employee_id': not self.env.user.has_group(
                'hr_timesheet.group_timesheet_manager')
        }
        return action
