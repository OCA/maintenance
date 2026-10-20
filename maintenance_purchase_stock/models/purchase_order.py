# Copyright 2025 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _get_lines_to_create_equipments(self):
        return (
            super()
            ._get_lines_to_create_equipments()
            .filtered(lambda x: x.qty_received > len(x.equipment_ids))
        )


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _qty_to_create_equipments(self):
        return int(self.qty_received - len(self.equipment_ids))
