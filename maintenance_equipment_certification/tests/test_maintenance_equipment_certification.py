# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase

_PARAM_ENABLED = "maintenance_equipment_certification.expiration_notify_enabled"


class TestMaintenanceEquipmentCertification(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_demo = cls.env["res.users"].create(
            {
                "name": "Demo User",
                "login": "demo_cert",
                "email": "demo@user.com",
                "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
            }
        )
        cls.technician = cls.env["res.users"].create(
            {
                "name": "Technician",
                "login": "tech_cert",
                "email": "tech@example.com",
                "group_ids": [
                    (6, 0, [cls.env.ref("maintenance.group_equipment_manager").id]),
                ],
            }
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "Test equipment",
                "technician_user_id": cls.technician.id,
            }
        )
        cls.env["ir.config_parameter"].sudo().set_param(_PARAM_ENABLED, "True")
        cls.rule_30 = cls.env["maintenance.certificate.reminder.rule"].create(
            {"name": "30 Days Before", "days_before": 30}
        )

    # --------
    # Helpers
    # --------

    def _make_certificate(self, renewal_offset_days, **kwargs):
        today = fields.Date.context_today(self.env["maintenance.equipment.certificate"])
        vals = {
            "name": "Test Certificate",
            "certificate_number": "CERT-001",
            "equipment_id": self.equipment.id,
            "date": today - timedelta(days=365),
            "renewal_date": today + timedelta(days=renewal_offset_days),
        }
        vals.update(kwargs)
        return self.env["maintenance.equipment.certificate"].create(vals)

    def _run_cron(self):
        self.env[
            "maintenance.equipment.certificate"
        ]._cron_notify_expiring_certificates()

    def _shift_renewal(self, cert, offset_days):
        cert.renewal_date = fields.Date.context_today(cert) + timedelta(
            days=offset_days
        )

    # ------------------------------------------------------------------
    # 1. Access control
    # ------------------------------------------------------------------

    def test_access_control(self):
        """A plain user cannot edit equipment; granting the maintenance
        manager group unlocks write access."""
        with self.assertRaises(AccessError):
            self.equipment.with_user(self.user_demo).name = "rename blocked"

        self.user_demo.write(
            {
                "group_ids": [
                    (6, 0, [self.env.ref("maintenance.group_equipment_manager").id])
                ],
            }
        )
        self.equipment.with_user(self.user_demo).name = "rename allowed"
        self.assertEqual(self.equipment.name, "rename allowed")

    # ------------------------------------------------------------------
    # 2. Full notification lifecycle (happy path + multi-rule + reset +
    #    idempotency)
    # ------------------------------------------------------------------

    def test_full_notification_lifecycle(self):
        """End-to-end flow: progressively crossing reminder thresholds
        increments notify_count once per rule, re-running the cron is a
        no-op, and pushing the renewal date out resets and re-arms the
        cycle."""
        rule_7 = self.env["maintenance.certificate.reminder.rule"].create(
            {"name": "7 Days Before", "days_before": 7}
        )
        rule_1 = self.env["maintenance.certificate.reminder.rule"].create(
            {"name": "1 Day Before", "days_before": 1}
        )

        # 25 days out: only the 30-day rule has triggered.
        cert = self._make_certificate(25)
        self._run_cron()
        self.assertEqual(cert.expiration_notify_count, 1)

        # 5 days out: 30-day + 7-day rules now triggered.
        self._shift_renewal(cert, 5)
        cert.write({"expiration_notify_count": 1})  # reset clears; re-seed
        self._run_cron()
        self.assertEqual(cert.expiration_notify_count, 2)

        # 1 day out: all three rules triggered.
        self._shift_renewal(cert, 1)
        cert.write({"expiration_notify_count": 2})
        self._run_cron()
        self.assertEqual(cert.expiration_notify_count, 3)

        # Idempotency: running the cron again sends nothing more.
        self._run_cron()
        self.assertEqual(cert.expiration_notify_count, 3)

        # Pushing the renewal date out resets the counter and re-arms
        # the 30-day rule on the next cron run.
        self._shift_renewal(cert, 20)
        self.assertEqual(cert.expiration_notify_count, 0)
        self._run_cron()
        self.assertEqual(cert.expiration_notify_count, 1)

        rule_7.unlink()
        rule_1.unlink()

    # ------------------------------------------------------------------
    # 3. Cron guard conditions — every reason the cron should do nothing
    # ------------------------------------------------------------------

    def test_cron_guard_conditions(self):
        """The cron must NOT create a notification when: the feature is
        disabled, no rules exist, the certificate is already expired, it
        is too far in the future, or the equipment has no responsible
        user."""
        with self.subTest("feature disabled"):
            self.env["ir.config_parameter"].sudo().set_param(_PARAM_ENABLED, "False")
            cert = self._make_certificate(10)
            self._run_cron()
            self.assertEqual(cert.expiration_notify_count, 0)
            self.env["ir.config_parameter"].sudo().set_param(_PARAM_ENABLED, "True")
            cert.unlink()

        with self.subTest("no reminder rules"):
            self.rule_30.unlink()
            cert = self._make_certificate(10)
            self._run_cron()
            self.assertEqual(cert.expiration_notify_count, 0)
            cert.unlink()
            self.__class__.rule_30 = self.env[
                "maintenance.certificate.reminder.rule"
            ].create({"name": "30 Days Before", "days_before": 30})

        with self.subTest("certificate already expired"):
            cert = self._make_certificate(-5)
            self._run_cron()
            self.assertEqual(cert.expiration_notify_count, 0)
            cert.unlink()

        with self.subTest("certificate too far in the future"):
            cert = self._make_certificate(60)
            self._run_cron()
            self.assertEqual(cert.expiration_notify_count, 0)
            cert.unlink()

        with self.subTest("equipment has no responsible user"):
            equipment_no_user = self.env["maintenance.equipment"].create(
                {"name": "Unassigned Equipment"}
            )
            cert = self._make_certificate(10, equipment_id=equipment_no_user.id)
            self._run_cron()
            self.assertEqual(cert.expiration_notify_count, 0)
