# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _prepare_new_request_activity_values(self, request, activity):
        """Prepare the values to create a new mail.activity for a maintenance request
        created from a maintenance plan.
        """
        return {
            "activity_type_id": activity.activity_type_id.id,
            "note": _("Activity automatically generated from maintenance plan"),
            "user_id": activity.user_id.id or self.env.user.id,
            "res_id": request.id,
            "res_model_id": self.env.ref("maintenance.model_maintenance_request").id,
            "date_deadline": request.schedule_date
            - timedelta(days=activity.date_before_request),
        }

    def _create_new_request(self, maintenance_plan):
        new_requests = super()._create_new_request(maintenance_plan)
        for request in new_requests:
            for planned_activity in maintenance_plan.planned_activity_ids:
                # In case mail_activity_team is installed this makes sure
                # the correct activity team is selected. If that module is
                # not installed the context does nothing
                activity_data = self._prepare_new_request_activity_values(
                    request, planned_activity
                )
                if activity_data:
                    self.env["mail.activity"].with_context(
                        default_res_model="maintenance.request"
                    ).create(activity_data)
        return new_requests
