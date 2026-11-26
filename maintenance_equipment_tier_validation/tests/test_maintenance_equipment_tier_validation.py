# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import new_test_user, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestMaintenanceEquipmentTierValidation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reviewer = new_test_user(
            cls.env,
            login="equipment_reviewer",
            groups="maintenance.group_equipment_manager",
        )
        cls.requester = new_test_user(
            cls.env,
            login="equipment_requester",
            groups="maintenance.group_equipment_manager",
        )
        cls.env["tier.definition"].create(
            {
                "model_id": cls.env["ir.model"]._get_id("maintenance.equipment"),
                "review_type": "individual",
                "reviewer_id": cls.reviewer.id,
                "definition_domain": "[]",
            }
        )
        cls.equipment = (
            cls.env["maintenance.equipment"]
            .with_user(cls.requester)
            .create({"name": "Test Equipment"})
        )

    def test_tier_validation_model_name(self):
        self.assertIn(
            "maintenance.equipment",
            self.env["tier.definition"]._get_tier_validation_model_names(),
        )

    def test_validate_equipment(self):
        self.assertTrue(self.equipment.need_validation)
        with self.assertRaises(ValidationError):
            self.equipment.action_validate_equipment()
        self.equipment.request_validation()
        self.equipment.with_user(self.reviewer).validate_tier()
        self.assertEqual(self.equipment.validation_status, "validated")
        self.equipment.invalidate_recordset()
        self.equipment.action_validate_equipment()
        self.assertEqual(self.equipment.state, "confirmed")

    def test_cancel_and_reset_to_draft(self):
        self.equipment.request_validation()
        self.equipment.action_cancel()
        self.assertEqual(self.equipment.state, "cancel")
        self.assertFalse(self.equipment.review_ids)
        self.equipment.action_reset_to_draft()
        self.assertEqual(self.equipment.state, "draft")
        self.assertTrue(self.equipment.need_validation)

    def test_existing_equipment_confirmed_on_install(self):
        equipment = self.env.ref("maintenance.equipment_monitor1", False)
        if not equipment:
            self.skipTest("Requires maintenance demo data")
        self.assertEqual(equipment.state, "confirmed")

    def test_validate_skips_cancelled_equipment(self):
        self.equipment.action_cancel()
        self.equipment.action_validate_equipment()
        self.assertEqual(self.equipment.state, "cancel")

    def test_cancel_validated_with_after_validation_exception(self):
        location = self.env["ir.model.fields"]._get("maintenance.equipment", "location")
        # Any exception enables the after-validation write check.
        self.env["tier.validation.exception"].create(
            {
                "model_id": location.model_id.id,
                "field_ids": [Command.link(location.id)],
                "allowed_to_write_after_validation": True,
            }
        )
        self.equipment.request_validation()
        self.equipment.with_user(self.reviewer).validate_tier()
        self.equipment.invalidate_recordset()
        self.equipment.action_validate_equipment()
        self.equipment.action_cancel()
        self.assertEqual(self.equipment.state, "cancel")
