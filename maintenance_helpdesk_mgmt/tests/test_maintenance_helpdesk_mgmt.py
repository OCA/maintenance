# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestMaintenanceHelpdeskMgmt(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.equipment = cls.env["maintenance.equipment"].create(
            {"name": "Test Equipment"}
        )
        cls.request = cls.env["maintenance.request"].create(
            {"name": "Test Request", "equipment_id": cls.equipment.id}
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {"name": "Test Ticket", "description": "Test description"}
        )

    def test_compute_count_zero(self):
        self.assertEqual(self.request.helpdesk_ticket_count, 0)
        self.assertEqual(self.ticket.maintenance_request_count, 0)

    def test_link_request_and_ticket(self):
        self.request.helpdesk_ticket_ids = [(4, self.ticket.id)]
        self.assertEqual(self.request.helpdesk_ticket_count, 1)
        self.assertEqual(self.ticket.maintenance_request_count, 1)

    def test_action_view_helpdesk_tickets_single(self):
        self.request.helpdesk_ticket_ids = [(4, self.ticket.id)]
        action = self.request.action_view_helpdesk_tickets()
        self.assertEqual(action["res_id"], self.ticket.id)
        self.assertEqual(action["views"], [(False, "form")])

    def test_action_view_helpdesk_tickets_multi(self):
        ticket_2 = self.env["helpdesk.ticket"].create(
            {"name": "Test Ticket 2", "description": "Test description 2"}
        )
        self.request.helpdesk_ticket_ids = [(4, self.ticket.id), (4, ticket_2.id)]
        action = self.request.action_view_helpdesk_tickets()
        self.assertIn(self.ticket.id, action["domain"][0][2])
        self.assertIn(ticket_2.id, action["domain"][0][2])

    def test_action_view_maintenance_request_single(self):
        self.ticket.maintenance_request_ids = [(4, self.request.id)]
        action = self.ticket.action_view_maintenance_request()
        self.assertEqual(action["res_id"], self.request.id)
        self.assertEqual(action["views"], [(False, "form")])

    def test_action_view_maintenance_request_multi(self):
        request_2 = self.env["maintenance.request"].create({"name": "Test Request 2"})
        self.ticket.maintenance_request_ids = [(4, self.request.id), (4, request_2.id)]
        action = self.ticket.action_view_maintenance_request()
        self.assertIn(self.request.id, action["domain"][0][2])
        self.assertIn(request_2.id, action["domain"][0][2])
