# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MaintenanceEquipmentCategory(models.Model):

    _inherit = "maintenance.equipment.category"

    equipment_scrap_template_id = fields.Many2one(
        "mail.template", string="Equipment Scrap Email Template",
    )
