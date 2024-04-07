# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import Form, SavepointCase


class TestEquipmentMeter(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {"name": "NEW USER", "login": "maintenenante_equipment_meter_test"}
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "My Equipment",
                "owner_user_id": cls.user.id,
                "meter_unit_id": cls.env.ref("uom.product_uom_km").id,
                "has_meter": True,
            }
        )
        cls.equipment_02 = cls.env["maintenance.equipment"].create(
            {
                "name": "My Equipment",
                "owner_user_id": cls.user.id,
                "meter_unit_id": cls.env.ref("uom.product_uom_km").id,
                "has_meter": True,
            }
        )

    def test_equipment(self):
        self.assertEqual(self.equipment.current_meter, 0.0)
        self.assertFalse(
            self.env["maintenance.equipment.meter"].search(
                [("equipment_id", "=", self.equipment.id)]
            )
        )
        self.equipment.current_meter = 1000.0
        self.assertTrue(
            self.env["maintenance.equipment.meter"].search(
                [("equipment_id", "=", self.equipment.id)]
            )
        )
        self.assertEqual(
            1000.0,
            self.env["maintenance.equipment.meter"]
            .search([("equipment_id", "=", self.equipment.id)])
            .value,
        )
        self.equipment.invalidate_cache()
        self.assertEqual(self.equipment.current_meter, 1000.0)

    def test_request(self):
        self.assertEqual(self.equipment.current_meter, 0.0)
        self.assertFalse(
            self.env["maintenance.equipment.meter"].search(
                [("equipment_id", "=", self.equipment.id)]
            )
        )

        with Form(self.env["maintenance.request"].with_user(self.user.id)) as f:
            f.equipment_id = self.equipment
            f.name = "DEMO Equipment"
            self.assertTrue(f.has_meter)
            f.current_meter = 1000.0
        request = f.save()
        self.assertEqual(
            1,
            len(
                self.env["maintenance.equipment.meter"].search(
                    [("equipment_id", "=", self.equipment.id)]
                )
            ),
        )
        self.assertEqual(
            1000.0,
            self.env["maintenance.equipment.meter"]
            .search([("equipment_id", "=", self.equipment.id)])
            .value,
        )
        self.assertTrue(request.meter_id)
        self.equipment.invalidate_cache()
        self.assertEqual(self.equipment.current_meter, 1000.0)
        with Form(request) as f:
            f.equipment_id = self.equipment_02
        self.assertFalse(request.meter_id)

    def test_request_exception(self):
        self.assertEqual(self.equipment.current_meter, 0.0)
        self.assertFalse(
            self.env["maintenance.equipment.meter"].search(
                [("equipment_id", "=", self.equipment.id)]
            )
        )

        with Form(self.env["maintenance.request"].with_user(self.user.id)) as f:
            f.equipment_id = self.equipment
            f.name = "DEMO Equipment"
            self.assertTrue(f.has_meter)
            f.current_meter = 1000.0
        request = f.save()
        self.assertEqual(
            1,
            len(
                self.env["maintenance.equipment.meter"].search(
                    [("equipment_id", "=", self.equipment.id)]
                )
            ),
        )
        self.assertEqual(
            1000.0,
            self.env["maintenance.equipment.meter"]
            .search([("equipment_id", "=", self.equipment.id)])
            .value,
        )
        self.assertTrue(request.meter_id)
        self.equipment.invalidate_cache()
        self.assertEqual(self.equipment.current_meter, 1000.0)
        with self.assertRaises(UserError):
            request.current_meter = 0.0
