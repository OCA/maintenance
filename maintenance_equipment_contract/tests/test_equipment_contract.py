# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestEquipmentContract(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test partner"})
        self.equipment_id = self.env["maintenance.equipment"].create(
            {"name": "Equipment"}
        )
        self.contract = self.env["contract.contract"].create(
            {
                "name": "Contract",
                "partner_id": self.partner.id,
                "equipment_ids": [(4, self.equipment_id.id)],
            }
        )

    def test_equipment_contract(self):
        self.assertEqual(self.equipment_id.contract_count, 1)
        action = self.equipment_id.action_view_contracts()
        self.assertEqual(action["res_id"], self.contract.id)

        self.env["contract.contract"].create(
            {
                "name": "Contract 2",
                "partner_id": self.partner.id,
                "equipment_ids": [(4, self.equipment_id.id)],
            }
        )
        self.assertEqual(self.equipment_id.contract_count, 2)
        action = self.equipment_id.action_view_contracts()
        self.assertIn("domain", action.keys())
