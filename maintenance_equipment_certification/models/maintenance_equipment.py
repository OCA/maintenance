# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    certificate_ids = fields.One2many(
        comodel_name="maintenance.equipment.certificate",
        inverse_name="equipment_id",
        string="Certificates",
    )
