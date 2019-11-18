# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    def _prepare_request_from_plan(
        self, maintenance_plan, next_maintenance_date
    ):
        res = super()._prepare_request_from_plan(
            maintenance_plan, next_maintenance_date
        )
        res.update({"tag_ids": [(6, 0, maintenance_plan.tag_ids.ids)]})
        return res
