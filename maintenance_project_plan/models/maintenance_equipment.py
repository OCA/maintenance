# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        request = super()._prepare_request_from_plan(
            maintenance_plan, next_maintenance_date
        )
        if maintenance_plan.project_id:
            request["project_id"] = maintenance_plan.project_id.id
        if maintenance_plan.task_id:
            request["task_id"] = maintenance_plan.task_id.id

        return request
