# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        tracking=True,
        domain="[('categ_id','=',product_category_id),('maintenance_ok','=',True)]",
    )
    product_category_id = fields.Many2one(
        comodel_name="product.category", related="category_id.product_category_id"
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """If product is set, equipment name, seller, seller ref and cost defaults
        to product ones.
        """
        if self.product_id:
            self.name = self.product_id.name
            self.cost = self.product_id.standard_price
            if self.product_id.seller_ids:
                first_seller = fields.first(self.product_id.seller_ids)
                self.partner_id = first_seller.partner_id
                self.partner_ref = first_seller.product_code


class MaintenanceEquipmentCategory(models.Model):
    _inherit = "maintenance.equipment.category"

    product_category_id = fields.Many2one(
        comodel_name="product.category", string="Product Category", tracking=True
    )

    @api.onchange("product_category_id")
    def _onchange_product_category_id(self):
        if self.product_category_id:
            self.name = self.product_category_id.name
