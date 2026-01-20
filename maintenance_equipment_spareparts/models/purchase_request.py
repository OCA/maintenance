# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        string="Equipment",
        help="When set, product selection will be restricted to spare parts "
        "registered for this equipment",
    )


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        string="Equipment",
        related="request_id.equipment_id",
        store=True,
        readonly=True,
    )

    @api.onchange("request_id")
    def _onchange_request_id(self):
        """Restrict product domain when equipment is set."""
        domain = [("purchase_ok", "=", True)]
        if self.request_id and self.request_id.equipment_id:
            sparepart_products = self.request_id.equipment_id.sparepart_ids.mapped(
                "product_id"
            )
            if sparepart_products:
                domain.append(("id", "in", sparepart_products.ids))
            else:
                # No spareparts registered, show empty domain to prevent selection
                domain.append(("id", "=", False))
        return {"domain": {"product_id": domain}}

    @api.constrains("equipment_id", "product_id")
    def _check_product_is_sparepart(self):
        """Ensure product is a registered spare part when equipment is set."""
        for record in self:
            if record.equipment_id and record.product_id:
                sparepart = self.env["maintenance.equipment.sparepart"].search(
                    [
                        ("equipment_id", "=", record.equipment_id.id),
                        ("product_id", "=", record.product_id.id),
                        ("active", "=", True),
                    ],
                    limit=1,
                )
                if not sparepart:
                    raise ValidationError(
                        _(
                            "Product %(product)s must be registered as a spare "
                            "part for equipment %(equipment)s before it can be "
                            "requested. Please add it as a spare part first."
                        )
                        % {
                            "product": record.product_id.display_name,
                            "equipment": record.equipment_id.display_name,
                        }
                    )
