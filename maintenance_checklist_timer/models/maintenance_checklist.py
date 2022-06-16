# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, _


class MaintenanceChecklist(models.Model):
    _name = 'maintenance.checklist'
    _inherit = ['maintenance.checklist', 'timer.mixin']

    def confirm_checklist(self):
        if self.state != 'block' and not self.user_timer_id.timer_start:
            self.action_timer_start()
        else:
            self.action_timer_resume()
        return super().confirm_checklist()

    def mark_as_done(self):
        if self.user_timer_id.timer_start:
            minutes_spent = self.user_timer_id._get_minutes_spent()
            minimum_duration = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'hr_timesheet.timesheet_min_duration', 0))
            rounding = int(self.env['ir.config_parameter'].sudo().get_param(
                'hr_timesheet.timesheet_rounding', 0))
            minutes_spent = self._timer_rounding(minutes_spent,
                                                 minimum_duration, rounding)
            return self._action_open_new_timesheet(minutes_spent * 60 / 3600)
        return super().mark_as_done()

    def _action_open_new_timesheet(self, time_spent):
        return {
            "name": _("Confirm Time Spent"),
            "type": 'ir.actions.act_window',
            "res_model": 'maintenance.checklist.create.timesheet',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
                'active_id': self.id,
                'active_model': self._name,
                'default_time_spent': time_spent,
            },
        }

    def mark_as_hold(self):
        self.action_timer_pause()
        return super().mark_as_hold()
