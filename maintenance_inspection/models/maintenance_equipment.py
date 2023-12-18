# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        result = super()._prepare_request_from_plan(
            maintenance_plan, next_maintenance_date
        )
        if maintenance_plan.inspection_item_ids:
            result.update(
                {
                    "has_inspection": True,
                    "inspection_line_ids": [
                        (
                            0,
                            0,
                            {
                                "item_id": item.id,
                            },
                        )
                        for item in maintenance_plan.inspection_item_ids
                    ],
                }
            )
        return result
