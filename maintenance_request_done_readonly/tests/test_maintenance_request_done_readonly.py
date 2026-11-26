# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, new_test_user


class TestMaintenanceRequestDoneReadonly(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.done_stage = cls.env["maintenance.stage"].search(
            [("done", "=", True)], limit=1
        )
        cls.open_stage = cls.env["maintenance.stage"].search(
            [("done", "=", False)], order="sequence", limit=1
        )
        cls.manager = new_test_user(
            cls.env,
            login="mrl_manager",
            groups="maintenance.group_equipment_manager",
        )
        cls.user = new_test_user(
            cls.env,
            login="mrl_user",
            groups="base.group_user",
        )
        cls.editor = new_test_user(
            cls.env,
            login="mrl_editor",
            groups="base.group_user,"
            "maintenance_request_done_readonly.group_maintenance_request_edit_done",
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {"name": "Test Equipment"}
        )

    def _new_request(self, user):
        # Regular users only see requests they own, follow or are assigned to
        # (record rule "equipment_request_rule_user"). Set ``user_id``, not
        # ``owner_user_id``: hr_maintenance (installed in CI) makes
        # ``owner_user_id`` a read-only computed field, so the value would be
        # ignored and the user would fail the rule on their own create.
        return (
            self.env["maintenance.request"]
            .with_user(user)
            .create(
                {
                    "name": "Test Request",
                    "equipment_id": self.equipment.id,
                    "user_id": user.id,
                    "stage_id": self.open_stage.id,
                }
            )
        )

    def test_regular_user_can_complete(self):
        """Completing a request (moving it to a done stage) is allowed for a
        regular user and must not be blocked by the lock guard."""
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        self.assertTrue(request.done)

    def test_regular_user_cannot_edit_completed(self):
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        with self.assertRaises(UserError):
            request.with_user(self.user).write({"name": "Changed"})

    def test_regular_user_cannot_reopen_completed(self):
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        with self.assertRaises(UserError):
            request.with_user(self.user).write({"stage_id": self.open_stage.id})

    def test_regular_user_can_edit_open(self):
        request = self._new_request(self.user)
        request.with_user(self.user).write({"name": "Still editable"})
        self.assertEqual(request.name, "Still editable")

    def test_manager_can_edit_completed(self):
        """Equipment managers imply the edit group, so they keep full access."""
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        request.with_user(self.manager).write({"name": "Corrected by manager"})
        self.assertEqual(request.name, "Corrected by manager")

    def test_editor_can_edit_completed(self):
        """A user granted the edit group, but not a manager, can still correct a
        completed request."""
        self.assertFalse(self.editor.has_group("maintenance.group_equipment_manager"))
        request = self._new_request(self.editor)
        request.with_user(self.editor).write({"stage_id": self.done_stage.id})
        request.with_user(self.editor).write({"name": "Corrected by editor"})
        self.assertEqual(request.name, "Corrected by editor")

    def test_configured_field_writable_when_done(self):
        """A field selected in the settings becomes writable again on a
        completed request, even for a regular user."""
        self.env["ir.config_parameter"].sudo().set_param(
            "maintenance_request_done_readonly.editable_fields", "close_date"
        )
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        request.with_user(self.user).write({"close_date": "2026-01-01"})
        self.assertEqual(str(request.close_date), "2026-01-01")

    def test_regular_user_can_comment_with_attachment_when_completed(self):
        """Posting in the chatter, with an attachment, must not be blocked on
        a completed request."""
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        attachment = (
            self.env["ir.attachment"]
            .with_user(self.user)
            .create(
                {
                    "name": "report.pdf",
                    "raw": b"%PDF-1.4",
                    "mimetype": "application/pdf",
                    "res_model": request._name,
                    "res_id": request.id,
                }
            )
        )
        message = request.with_user(self.user).message_post(
            body="Still can comment", attachment_ids=attachment.ids
        )
        self.assertEqual(message.attachment_ids, attachment)

    def test_regular_user_cannot_delete_completed(self):
        request = self._new_request(self.user)
        request.with_user(self.user).write({"stage_id": self.done_stage.id})
        with self.assertRaises(UserError):
            request.with_user(self.user).unlink()
        self.assertTrue(request.exists())

    def test_regular_user_can_delete_open(self):
        request = self._new_request(self.user)
        request.with_user(self.user).unlink()
        self.assertFalse(request.exists())

    def test_editor_can_delete_completed(self):
        request = self._new_request(self.editor)
        request.with_user(self.editor).write({"stage_id": self.done_stage.id})
        request.with_user(self.editor).unlink()
        self.assertFalse(request.exists())
