# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from datetime import timedelta


class MaintenancePlan(models.Model):
    _inherit = 'maintenance.plan'

    planned_activity_ids = fields.One2many(
        'maintenance.planned.activity', 'maintenance_plan_id',
        'Planned Activities'
    )


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    def _create_new_request(self, maintenance_plan):
        new_requests = super()._create_new_request(maintenance_plan)
        maintenance_model = self.env.ref(
            'maintenance.model_maintenance_request')
        for request in new_requests:
            for planned_activity in maintenance_plan.planned_activity_ids:
                # In case mail_activty_team is installed this makes sure
                # the correct activity team is selected. If that module is
                # not installed the context does nothing
                self.env['mail.activity'].with_context(
                    default_res_model='maintenance.request').create(
                    {
                        'activity_type_id': planned_activity.activity_type_id.id,
                        'note': _(
                            'Activity automatically generated from '
                            'maintenance plan'),
                        'user_id': planned_activity.user_id.id or self.env.user.id,
                        'res_id': request.id,
                        'res_model_id': maintenance_model.id,
                        'date_deadline': fields.Date.from_string(
                            request.schedule_date) -
                        timedelta(
                            days=planned_activity.date_before_request),
                    })
        return new_requests
