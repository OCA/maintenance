# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenancePartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "Test Equipment",
            }
        )

    def test_partner_from_equipment(self):
        # While it is not assigned, the request is not assigned to the partner
        request_01 = self.env["maintenance.request"].create(
            {
                "name": "Test Request",
                "equipment_id": self.equipment.id,
            }
        )
        self.assertFalse(request_01.partner_id)
        # When assigned, the request is assigned to the partner
        self.equipment.assigned_partner_id = self.partner
        request_02 = self.env["maintenance.request"].create(
            {
                "name": "Test Request",
                "equipment_id": self.equipment.id,
            }
        )
        self.assertEqual(
            request_02.partner_id,
            self.partner,
        )
        # Original requests shouldn't be changed
        request_01.invalidate_recordset()
        self.assertFalse(request_01.partner_id)

    def test_request_counter(self):
        self.assertEqual(self.partner.maintenance_request_count, 0)
        self.env["maintenance.request"].create(
            {
                "name": "Test Request",
                "partner_id": self.partner.id,
            }
        )
        self.assertEqual(self.partner.maintenance_request_count, 1)

    def test_equipment_counter(self):
        self.assertEqual(self.partner.equipment_count, 0)
        self.equipment.assigned_partner_id = self.partner
        self.assertEqual(self.partner.equipment_count, 1)
