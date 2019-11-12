# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenanceRequestDuplicated(TransactionCase):

    def setUp(self):
        super().setUp()
        self.team = self.env['maintenance.team'].create({
            'name': 'Team 1'
        })
        self.m_request_1 = self.env['maintenance.request'].create({
            'name': 'Request 1',
            'maintenance_team_id': self.team.id,
        })
        self.m_request_2 = self.env['maintenance.request'].create({
            'name': 'Request 2',
            'maintenance_team_id': self.team.id,
        })

    def test_maintenance_request_duplicated(self):
        wizz = self.env['wizard.request.duplicated'].create({
            'duplicated_request': self.m_request_2.id,
            'original_request': self.m_request_1.id,
        })
        wizz.mark_as_duplicated()
        self.assertTrue(self.m_request_1.child_ids)
        self.assertEqual(self.m_request_2.parent_id, self.m_request_1)

        self.m_request_2.deduplicate()
        self.assertFalse(self.m_request_2.parent_id)
