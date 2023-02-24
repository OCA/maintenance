# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        res = super()._prepare_request_from_plan(
            maintenance_plan=maintenance_plan,
            next_maintenance_date=next_maintenance_date,
        )
        if maintenance_plan.employee_ids:
            res["employee_ids"] = [(6, 0, maintenance_plan.employee_ids.ids)]
        return res
