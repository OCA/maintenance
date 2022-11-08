# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestRequestTags(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        self = cls
        self.tag_1 = self.env["maintenance.request.tag"].create({"name": "Test Tag 1"})
        self.tag_2 = self.env["maintenance.request.tag"].create({"name": "Test Tag 2"})
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
        self.equipment = self.env["maintenance.equipment"].create({"name": "Laptop"})

        self.plan = self.env["maintenance.plan"].create(
            {
                "equipment_id": self.equipment.id,
                "interval": 1,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
                "maintenance_team_id": self.team_2.id,
                "tag_ids": [(4, self.tag_2.id)],
            }
        )

    def test_request_tags(self):
        request = self.env["maintenance.request"].create(
            {"name": "Request", "maintenance_team_id": self.team_2.id}
        )
        self.assertEqual(len(request.selectable_tags_ids), 2)

    def test_request_creation(self):
        request = self.equipment._create_new_request(self.plan)
        self.assertTrue(request)
        for r in request:
            self.assertTrue(r.tag_ids)
