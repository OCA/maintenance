# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


# This test should only be executed after all modules have been installed.
@tagged("post_install", "-at_install")
class TestTeamHierarchy(TransactionCase):
    def setUp(self):
        super().setUp()
        self.team_obj = self.env["maintenance.team"]
        self.request_obj = self.env["maintenance.request"]

    def test_team_hierarchy(self):
        team_01 = self.team_obj.create({"name": "01"})
        team_02 = self.team_obj.create({"name": "02"})
        team_03 = self.team_obj.create({"name": "02"})
        self.assertFalse(team_01.request_ids)
        self.assertFalse(team_02.request_ids)
        self.assertFalse(team_03.request_ids)
        self.assertEqual(0, team_01.todo_request_count)
        self.assertEqual(0, team_02.todo_request_count)
        self.assertEqual(0, team_03.todo_request_count)
        request_01 = self.request_obj.create(
            {"name": "Request", "maintenance_team_id": team_03.id}
        )
        team_01.refresh()
        team_02.refresh()
        team_03.refresh()
        self.assertFalse(team_01.request_ids)
        self.assertFalse(team_02.request_ids)
        self.assertTrue(team_03.request_ids)
        self.assertEqual(0, team_01.todo_request_count)
        self.assertEqual(0, team_02.todo_request_count)
        self.assertEqual(1, team_03.todo_request_count)
        self.assertEqual(request_01, team_03.request_ids)
        team_03.write({"parent_id": team_02.id})
        team_01.refresh()
        team_02.refresh()
        team_03.refresh()
        self.assertFalse(team_01.request_ids)
        self.assertTrue(team_02.request_ids)
        self.assertEqual(team_02.request_ids, request_01)
        self.assertEqual(0, team_01.todo_request_count)
        self.assertEqual(1, team_02.todo_request_count)
        self.assertEqual(1, team_03.todo_request_count)
        request_02 = self.request_obj.create(
            {"name": "Request", "maintenance_team_id": team_02.id}
        )
        team_01.refresh()
        team_02.refresh()
        team_03.refresh()
        self.assertFalse(team_01.request_ids)
        self.assertTrue(team_02.request_ids)
        self.assertIn(request_01, team_02.request_ids)
        self.assertIn(request_02, team_02.request_ids)
        self.assertTrue(team_03.request_ids)
        self.assertEqual(request_01, team_03.request_ids)
        self.assertNotIn(request_02, team_03.request_ids)
        self.assertEqual(0, team_01.todo_request_count)
        self.assertEqual(2, team_02.todo_request_count)
        self.assertEqual(1, team_03.todo_request_count)
        team_02.write({"parent_id": team_01.id})
        team_01.refresh()
        team_02.refresh()
        team_03.refresh()
        self.assertIn(request_01, team_01.request_ids)
        self.assertIn(request_02, team_01.request_ids)
        self.assertEqual(2, team_01.todo_request_count)
        self.assertEqual(2, team_02.todo_request_count)
        self.assertEqual(1, team_03.todo_request_count)
