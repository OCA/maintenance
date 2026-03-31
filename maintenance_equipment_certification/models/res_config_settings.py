# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cert_expiration_notify_enabled = fields.Boolean(
        string="Certificate Expiration Alert",
        config_parameter="maintenance_equipment_certification.expiration_notify_enabled",
        help="Send an email notification when a certificate is about to expire.",
    )
