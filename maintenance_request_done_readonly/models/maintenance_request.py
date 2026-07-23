# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    def _writable_fields_when_done(self):
        """Fields a user without the edit group may still write when completed.

        ``message_main_attachment_id`` is written by the chatter when a file is
        attached, so it is always allowed to keep commenting with attachments
        working. Extra fields come from the
        ``maintenance_request_done_readonly.editable_fields`` system parameter;
        every other field is locked.
        """
        names = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("maintenance_request_done_readonly.editable_fields", "")
        )
        return {"message_main_attachment_id"} | {
            name.strip() for name in names.split(",") if name.strip()
        }

    def write(self, vals):
        # A completed (done) request can only be edited by users in the edit
        # group. Checked pre-write, so everyone can still complete a request
        # (move it to done).
        if (
            not self.env.context.get("mnt_done_bypass_lock")
            and not self.env.user.has_group(
                "maintenance_request_done_readonly."
                "group_maintenance_request_edit_done"
            )
            and (set(vals) - self._writable_fields_when_done())
            and (locked := self.filtered("done"))
        ):
            raise UserError(
                _(
                    "'%s' is completed and can only be edited by users in the "
                    "'Maintenance: Edit Completed Requests' group.",
                    locked[0].display_name,
                )
            )
        # When completing a request, let the internal close_date write (done by
        # core maintenance) bypass the lock above so completion isn't blocked.
        stage_id = vals.get("stage_id")
        if stage_id and self.env["maintenance.stage"].browse(stage_id).done:
            self = self.with_context(mnt_done_bypass_lock=True)
        return super().write(vals)
