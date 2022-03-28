# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    equipment_ids = fields.One2many(
        comodel_name="maintenance.equipment",
        inverse_name="product_id",
        string="Equipments",
    )
