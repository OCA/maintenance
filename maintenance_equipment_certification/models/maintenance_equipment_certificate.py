# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MaintenanceEquipmentCertificate(models.Model):
    _name = "maintenance.equipment.certificate"
    _description = "Maintenance equipment certificate"

    name = fields.Char()
    notes = fields.Text()
    date = fields.Date()
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
