# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    purchase_equipment_category_id = fields.Many2one(
        comodel_name="maintenance.equipment.category",
        string="Purchase Equipment Category",
    )
