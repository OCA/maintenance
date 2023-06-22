# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenanceRequestSequence(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team_id = cls.env["maintenance.team"].create(
            {"name": "Maintenance Team", "code_prefix": "MT-TEST"}
        )
        cls.team_id_2 = cls.env["maintenance.team"].create({"name": "Maintenance Team"})

    def test_maintenance_request_sequence(self):
        sequence = self.env["ir.sequence"].search([("prefix", "=", "MT-TEST")])
        self.assertTrue(sequence)

        self.assertFalse(self.team_id_2.sequence_id)
        self.team_id_2.write({"code_prefix": "TEAM2-TEST"})
        self.assertTrue(self.team_id_2.sequence_id)

        request_1 = self.env["maintenance.request"].create(
            {"name": "Req 1", "maintenance_team_id": self.team_id.id}
        )
        self.assertIn("MT-TEST", request_1.code)
        self.team_id.write({"code_prefix": "MT-TEST-2"})
        request_2 = self.env["maintenance.request"].create(
            {"name": "Req 2", "maintenance_team_id": self.team_id.id}
        )
        self.assertIn("MT-TEST-2", request_2.code)

        res = self.env["maintenance.request"].name_search(request_2.code)
        self.assertTrue(res)
