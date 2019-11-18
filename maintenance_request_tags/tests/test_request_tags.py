# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestRequestTags(TransactionCase):
    def setUp(self):
        super().setUp()
        self.tag_1 = self.env["maintenance.request.tag"].create(
            {"name": "Test Tag 1"}
        )
        self.tag_2 = self.env["maintenance.request.tag"].create(
            {"name": "Test Tag 2"}
        )
        self.team_1 = self.env["maintenance.team"].create(
            {"name": "T1", "selectable_tags_ids": [(4, self.tag_1.id)]}
        )
        self.team_2 = self.env["maintenance.team"].create(
            {
                "name": "T2",
                "selectable_tags_ids": [(4, self.tag_2.id)],
                "parent_id": self.team_1.id,
            }
        )

    def test_request_tags(self):
        request = self.env["maintenance.request"].create(
            {"name": "Request", "maintenance_team_id": self.team_2.id}
        )
        self.assertEqual(len(request.selectable_tags_ids), 2)
