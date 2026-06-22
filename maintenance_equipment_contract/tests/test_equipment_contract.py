# Copyright 2019 Creu Blanca
# Copyright 2026 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
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

    def test_contract_maintenance_requests(self):
        other_equipment = self.env["maintenance.equipment"].create(
            {"name": "Other equipment"}
        )
        request = self.env["maintenance.request"].create(
            {"name": "Request", "equipment_id": self.equipment_id.id}
        )
        other_request = self.env["maintenance.request"].create(
            {"name": "Other request", "equipment_id": other_equipment.id}
        )
        self.assertEqual(self.contract.equipment_count, 1)
        action = self.contract.action_show_maintenance_requests()
        requests = self.env["maintenance.request"].search(action["domain"])
        self.assertIn(request, requests)
        self.assertNotIn(other_request, requests)
