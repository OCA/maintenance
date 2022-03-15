# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    equipment_category_ids = fields.One2many(
        comodel_name="maintenance.equipment.category",
        inverse_name="product_category_id",
        string="Equipment Categories",
    )
