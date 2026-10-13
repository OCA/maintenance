# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import timedelta

from markupsafe import Markup, escape

from odoo import api, fields, models


class MaintenanceEquipmentCertificate(models.Model):
    _name = "maintenance.equipment.certificate"
    _description = "Maintenance equipment certificate"

    active = fields.Boolean(default=True)
    name = fields.Char()
    certificate_number = fields.Char()
    notes = fields.Text()
    date = fields.Date()
    renewal_date = fields.Date()
    certificate_file = fields.Binary(
        string="Certificate",
        attachment=True,
    )
    certificate_filename = fields.Char(
        string="Certificate file name",
    )
    equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
    )
    expiration_notify_count = fields.Integer(
        string="Notifications Sent",
        default=0,
        copy=False,
    )

    def write(self, vals):
        if "renewal_date" in vals:
            vals = dict(vals)
            vals.setdefault("expiration_notify_count", 0)
        return super().write(vals)

    @api.model
    def _cron_notify_expiring_certificates(self):
        ICP = self.env["ir.config_parameter"].sudo()
        enabled = ICP.get_param(
            "maintenance_equipment_certification.expiration_notify_enabled", False
        )
        if not enabled or enabled == "False":
            return False
        rules = self.env["maintenance.certificate.reminder.rule"].search(
            [], order="days_before desc", limit=False
        )
        if not rules:
            return False
        template = self.env.ref(
            "maintenance_equipment_certification.mail_template_certificate_expiration",
            raise_if_not_found=False,
        )
        today = fields.Date.context_today(self)
        max_days = rules[0].days_before
        deadline = today + timedelta(days=max_days)
        certificates = self.search(
            [
                ("renewal_date", "<=", deadline),
                ("renewal_date", ">=", today),
                ("expiration_notify_count", "<", len(rules)),
                ("equipment_id", "!=", False),
            ]
        )
        for cert in certificates:
            days_remaining = (cert.renewal_date - today).days
            # Count how many rules have triggered (days_before >= days_remaining)
            expected = sum(1 for r in rules if r.days_before >= days_remaining)
            if cert.expiration_notify_count >= expected:
                continue
            equipment = cert.equipment_id
            user = equipment.technician_user_id or equipment.owner_user_id
            if not user:
                equipment.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=cert.renewal_date,
                    summary=self.env._("Certificate expiration: no assignee to notify"),
                    note=Markup(
                        "Certificate <b>%s</b> (renewal: %s) could not send "
                        "expiration reminder: no technician or owner is assigned."
                    )
                    % (escape(cert.name), cert.renewal_date),
                )
                continue
            if template:
                template.send_mail(
                    cert.id,
                    email_layout_xmlid="mail.mail_notification_light",
                    email_values={"partner_ids": [user.partner_id.id]},
                )
                equipment.message_post(
                    body=Markup(
                        "Certificate expiration reminder sent for "
                        "<b>%s</b> (renewal: %s)."
                    )
                    % (escape(cert.name), cert.renewal_date),
                    subtype_xmlid="mail.mt_note",
                )
            cert.expiration_notify_count = expected
