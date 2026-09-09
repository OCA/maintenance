# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class CertificateReminderRule(models.Model):
    _name = "maintenance.certificate.reminder.rule"
    _description = "Certificate expiration reminder rule"
    _order = "days_before desc"

    name = fields.Char(
        string="Rule Name",
        required=True,
    )
    days_before = fields.Integer(
        string="Days Before Expiration",
        required=True,
        help="How many days before the renewal date to schedule the reminder.",
    )
