# Copyright 2021 Exo Software, Lda.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = ["maintenance.equipment", "image.mixin"]
    _name = "maintenance.equipment"
