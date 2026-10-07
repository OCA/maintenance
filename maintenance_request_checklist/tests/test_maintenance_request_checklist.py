# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestMaintenanceRequestChecklist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
            )
        )
        cls.ChecklistLine = cls.env["maintenance.request.checklist.line"]
        cls.request = cls.env["maintenance.request"].create({"name": "Test Request"})
        cls.line_vals = [
            {"name": "Check oil level", "sequence": 10},
            {"name": "Inspect belts", "sequence": 20},
            {"name": "Test brakes", "sequence": 30},
        ]

    def _create_lines(self, vals_list=None):
        vals = vals_list or self.line_vals
        return self.ChecklistLine.create(
            [dict(v, request_id=self.request.id) for v in vals]
        )

    def test_checklist_line_creation(self):
        lines = self._create_lines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines.mapped("request_id"), self.request)
        for line in lines:
            self.assertFalse(line.is_done)
            self.assertFalse(line.done_by)
            self.assertFalse(line.done_date)

    def test_mark_done_sets_audit_fields(self):
        line = self._create_lines([{"name": "Check oil level", "sequence": 10}])
        before = fields.Datetime.now()
        line.write({"is_done": True})
        after = fields.Datetime.now()

        self.assertTrue(line.is_done)
        self.assertEqual(line.done_by, self.env.user)
        self.assertTrue(line.done_date)
        self.assertGreaterEqual(line.done_date, before)
        self.assertLessEqual(line.done_date, after)

    def test_unmark_done_clears_audit_fields(self):
        line = self._create_lines([{"name": "Check oil level", "sequence": 10}])
        line.write({"is_done": True})
        self.assertTrue(line.is_done)

        line.write({"is_done": False})
        self.assertFalse(line.is_done)
        self.assertFalse(line.done_by)
        self.assertFalse(line.done_date)

    def test_done_by_not_overwritten_if_already_set(self):
        other_user = self.env["res.users"].create(
            {
                "name": "Mechanic",
                "login": "mechanic_test",
                "email": "mechanic@test.com",
            }
        )
        line = self._create_lines([{"name": "Check oil level", "sequence": 10}])
        line.write({"is_done": True, "done_by": other_user.id})
        # done_by explicitly passed should be respected (setdefault behaviour)
        self.assertEqual(line.done_by, other_user)

    def test_checklist_progress_counters(self):
        lines = self._create_lines()
        self.request.invalidate_recordset()
        self.assertEqual(self.request.checklist_total, 3)
        self.assertEqual(self.request.checklist_done, 0)

        lines[0].write({"is_done": True})
        self.request.invalidate_recordset()
        self.assertEqual(self.request.checklist_done, 1)

        lines[1].write({"is_done": True})
        self.request.invalidate_recordset()
        self.assertEqual(self.request.checklist_done, 2)

        lines[0].write({"is_done": False})
        self.request.invalidate_recordset()
        self.assertEqual(self.request.checklist_done, 1)

    def test_checklist_total_with_no_lines(self):
        request = self.env["maintenance.request"].create({"name": "Empty Request"})
        self.assertEqual(request.checklist_total, 0)
        self.assertEqual(request.checklist_done, 0)

    def test_sequence_ordering(self):
        lines = self.ChecklistLine.create(
            [
                {"request_id": self.request.id, "name": "Step C", "sequence": 30},
                {"request_id": self.request.id, "name": "Step A", "sequence": 10},
                {"request_id": self.request.id, "name": "Step B", "sequence": 20},
            ]
        )
        ordered = self.ChecklistLine.search(
            [("id", "in", lines.ids)], order="sequence asc"
        )
        self.assertEqual(ordered.mapped("name"), ["Step A", "Step B", "Step C"])

    def test_line_cascade_delete(self):
        lines = self._create_lines()
        request = lines[0].request_id
        line_ids = lines.ids
        request.unlink()
        remaining = self.ChecklistLine.search([("id", "in", line_ids)])
        self.assertFalse(remaining)
