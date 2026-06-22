# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestEquipmentContract(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.equipment_id = cls.env["maintenance.equipment"].create(
            {"name": "Equipment"}
        )
        cls.contract = cls.env["contract.contract"].create(
            {
                "name": "Contract",
                "partner_id": cls.partner.id,
                "equipment_ids": [Command.link(cls.equipment_id.id)],
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
                "equipment_ids": [Command.link(self.equipment_id.id)],
            }
        )
        self.assertEqual(self.equipment_id.contract_count, 2)
        action = self.equipment_id.action_view_contracts()
        self.assertIn("domain", action.keys())
