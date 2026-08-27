# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceEquipmentAvailability(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.equipment = cls.env["maintenance.equipment"].create(
            {"name": "Availability Test Equipment"}
        )
        cls.open_stage = cls.env.ref("maintenance.stage_0")
        cls.done_stage = cls.env.ref("maintenance.stage_3")

    def _create_request(
        self, stage, result="none", request_date="2024-01-01", close_date=False
    ):
        vals = {
            "name": f"Request {stage.name}",
            "equipment_id": self.equipment.id,
            "stage_id": stage.id,
            "request_date": request_date,
            "maintenance_result": result,
        }
        if close_date:
            vals["close_date"] = close_date
        return self.env["maintenance.request"].create(vals)

    def test_availability_unknown_without_completed_result(self):
        self.assertEqual(self.equipment.availability_state, "unknown")
        # A result on a request that is not done yet is ignored.
        self._create_request(self.open_stage, result="passed")
        self.assertEqual(self.equipment.availability_state, "unknown")
        # A done request without a result is ignored.
        self._create_request(self.done_stage, result="none", close_date="2024-01-01")
        self.assertEqual(self.equipment.availability_state, "unknown")
        self.assertFalse(self.equipment.latest_maintenance_result_request_id)
        self.assertFalse(self.equipment.latest_maintenance_result_date)

    def test_passed_makes_equipment_available(self):
        request = self._create_request(
            self.done_stage, result="passed", close_date="2024-01-01"
        )
        self.assertEqual(self.equipment.availability_state, "available")
        self.assertEqual(self.equipment.latest_maintenance_result_request_id, request)
        self.assertEqual(
            self.equipment.latest_maintenance_result_date.isoformat(), "2024-01-01"
        )

    def test_availability_uses_latest_result_by_close_date(self):
        self._create_request(self.done_stage, result="passed", close_date="2024-01-01")
        self.assertEqual(self.equipment.availability_state, "available")

        failed = self._create_request(
            self.done_stage,
            result="failed",
            request_date="2024-02-01",
            close_date="2024-01-10",
        )
        self.assertEqual(self.equipment.availability_state, "unavailable")
        self.assertEqual(self.equipment.latest_maintenance_result_request_id, failed)

        # An older close_date does not override the latest result.
        self._create_request(
            self.done_stage,
            result="passed",
            request_date="2024-03-01",
            close_date="2024-01-05",
        )
        self.assertEqual(self.equipment.availability_state, "unavailable")

    def test_create_followup_request_from_failed(self):
        request = self._create_request(
            self.done_stage, result="failed", close_date="2024-01-01"
        )
        request.action_create_followup_request()
        followup = request.followup_request_ids
        self.assertEqual(len(followup), 1)
        self.assertEqual(followup.source_request_id, request)
        self.assertEqual(followup.equipment_id, self.equipment)
        self.assertEqual(followup.maintenance_type, "corrective")
