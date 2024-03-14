# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMaintenancePurchase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.team_id = cls.env["maintenance.team"].create({"name": "Maintenance Team"})
        cls.request_1 = cls.env["maintenance.request"].create(
            {"name": "Req 1", "maintenance_team_id": cls.team_id.id}
        )
        cls.request_2 = cls.env["maintenance.request"].create(
            {"name": "Req 1", "maintenance_team_id": cls.team_id.id}
        )
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier"})
        cls.po_1 = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "date_planned": "2017-02-11 22:00:00",
            }
        )

    def test_maintenance_purchase(self):
        self.assertEqual(self.request_1.purchases_count, 0)
        self.assertEqual(self.po_1.maintenance_requests_count, 0)
        self.request_1.purchase_order_ids = self.po_1
        self.assertEqual(self.request_1.purchases_count, 1)
        self.assertEqual(self.po_1.maintenance_requests_count, 1)
        action = self.po_1.action_view_maintenance_request()
        self.assertEqual(action["res_id"], self.request_1.id)
        self.request_2.write({"purchase_order_ids": [(4, self.po_1.id)]})
        action = self.po_1.action_view_maintenance_request()
        requests = self.env[action["res_model"]].search(action["domain"])
        self.assertIn(self.request_1, requests)
        self.assertIn(self.request_2, requests)
