# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form
from odoo.tests.common import users

from odoo.addons.sign_oca.tests.common import TestSignOcaBase


class TestBaseTierValidationSign(TestSignOcaBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.equipment_a = cls.env["maintenance.equipment"].create(
            {"name": "Test equipment A", "owner_user_id": cls.sign_user.id}
        )
        cls.equipment_a.message_subscribe([cls.sign_user.partner_id.id])
        cls.equipment_b = cls.env["maintenance.equipment"].create(
            {"name": "Test equipment B", "owner_user_id": cls.sign_manager_user.id}
        )
        cls.equipment_b.message_subscribe([cls.sign_manager_user.partner_id.id])

    @users("test-sign-oca-user")
    def test_request_record_ref_onchange(self):
        request_form = Form(self.env["sign.request"])
        request_form.record_ref = "%s,%s" % (
            self.equipment_a._name,
            self.equipment_a.id,
        )
        request = request_form.save()
        self.assertEqual(request.partner_id, self.sign_user.partner_id)
        self.assertEqual(request.maintenance_equipment_id, self.equipment_a)
        self.assertIn(request, self.equipment_a.sign_request_ids)

    def test_request_equipments_wizard(self):
        equipments = self.equipment_a + self.equipment_b
        equipments_with_ctx = equipments.with_context(
            active_model=equipments._name, active_ids=equipments.ids
        )
        res = equipments_with_ctx.action_maintenance_equipment_sign_request()
        wizard_form = Form(self.env[res["res_model"]].with_context(res["context"]))
        wizard = wizard_form.save()
        self.assertIn(self.equipment_a, wizard.line_ids.mapped("record_ref"))
        self.assertIn(self.equipment_b, wizard.line_ids.mapped("record_ref"))
        res = wizard.action_process()
        items = self.env[res["res_model"]].search(res["domain"])
        self.assertEqual(len(items), 2)
        self.assertIn(self.equipment_a, items.mapped("maintenance_equipment_id"))
        self.assertIn(self.equipment_b, items.mapped("maintenance_equipment_id"))
