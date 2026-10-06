# Copyright 2026 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import new_test_user, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestMaintenanceEquipmentTierValidation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Equipment = cls.env["maintenance.equipment"]
        cls.TierDefinition = cls.env["tier.definition"]
        cls.equipment_model = cls.env["ir.model"]._get("maintenance.equipment")
        cls.reviewer = new_test_user(
            cls.env,
            name="Equipment Reviewer",
            login="equipment_reviewer",
            groups="base.group_system,maintenance.group_equipment_manager",
        )
        cls.requester = new_test_user(
            cls.env,
            name="Equipment Requester",
            login="equipment_requester",
            groups="base.group_system,maintenance.group_equipment_manager",
        )
        cls.TierDefinition.create(
            {
                "model_id": cls.equipment_model.id,
                "review_type": "individual",
                "reviewer_id": cls.reviewer.id,
                "definition_domain": "[]",
            }
        )

    def test_tier_validation_model_name(self):
        self.assertIn(
            "maintenance.equipment",
            self.TierDefinition._get_tier_validation_model_names(),
        )

    def test_validation_maintenance_equipment(self):
        equipment_to_block = self.Equipment.create({"name": "Equipment to block"})

        with self.assertRaises(ValidationError):
            equipment_to_block.with_user(self.requester).action_validate_equipment()

        equipment = self.Equipment.create({"name": "Equipment to validate"})

        self.assertEqual(equipment.state, "draft")
        self.assertTrue(equipment.need_validation)

        equipment.with_user(self.requester).request_validation()
        self.assertTrue(equipment.review_ids)

        equipment.with_user(self.reviewer).validate_tier()
        self.assertEqual(equipment.validation_status, "validated")

        equipment.invalidate_recordset()
        equipment.with_user(self.requester).action_validate_equipment()
        self.assertEqual(equipment.state, "confirmed")
