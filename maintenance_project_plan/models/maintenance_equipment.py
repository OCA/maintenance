# Copyright 2019 Solvos Consultor??a Inform??tica (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    def _prepare_request_from_plan(self, maintenance_plan):
        request = super()._prepare_request_from_plan(maintenance_plan)
        if maintenance_plan.project_id:
            request['project_id'] = maintenance_plan.project_id.id
        if maintenance_plan.task_id:
            request['task_id'] = maintenance_plan.task_id.id

        return request
