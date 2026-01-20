# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    sparepart_ids = fields.One2many(
        comodel_name="maintenance.equipment.sparepart",
        inverse_name="equipment_id",
        string="Spare Parts",
    )
    sparepart_count = fields.Integer(
        string="Spare Parts Count",
        compute="_compute_sparepart_count",
        store=True,
    )

    @api.depends("sparepart_ids")
    def _compute_sparepart_count(self):
        for record in self:
            record.sparepart_count = len(record.sparepart_ids.filtered("active"))

    def action_view_spareparts(self):
        self.ensure_one()
        action = {
            "name": "Spare Parts",
            "type": "ir.actions.act_window",
            "res_model": "maintenance.equipment.sparepart",
            "view_mode": "tree,form",
            "domain": [("equipment_id", "=", self.id)],
            "context": {"default_equipment_id": self.id},
        }
        return action

    def action_create_purchase_request(self):
        """Create purchase request for spare parts below recommended quantity."""
        self.ensure_one()
        spareparts_needing_reorder = self.sparepart_ids.filtered("needs_reorder")
        if not spareparts_needing_reorder:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("No Action Needed"),
                    "message": _("All spare parts have sufficient stock."),
                    "type": "success",
                },
            }
        picking_type = self.env["stock.picking.type"].search(
            [
                ("code", "=", "incoming"),
                ("warehouse_id.company_id", "=", self.company_id.id),
            ],
            limit=1,
        )
        if not picking_type:
            picking_type = self.env["stock.picking.type"].search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)], limit=1
            )
        purchase_request = self.env["purchase.request"].create(
            {
                "origin": _("Equipment: %s") % self.display_name,
                "requested_by": self.env.user.id,
                "company_id": self.company_id.id,
                "picking_type_id": picking_type.id if picking_type else False,
                "equipment_id": self.id,
            }
        )
        lines_created = False
        for sparepart in spareparts_needing_reorder:
            qty_needed = sparepart.spare_qty - sparepart.available_qty
            if qty_needed > 0:
                self.env["purchase.request.line"].create(
                    {
                        "request_id": purchase_request.id,
                        "product_id": sparepart.product_id.id,
                        "product_uom_id": sparepart.product_id.uom_id.id,
                        "product_qty": qty_needed,
                        "name": sparepart.product_id.display_name,
                    }
                )
                lines_created = True
        if not lines_created:
            # No lines were created, cancel the request
            purchase_request.unlink()
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("No Action Needed"),
                    "message": _("All spare parts have sufficient stock."),
                    "type": "success",
                },
            }
        return {
            "name": _("Purchase Request"),
            "type": "ir.actions.act_window",
            "res_model": "purchase.request",
            "view_mode": "form",
            "res_id": purchase_request.id,
            "target": "current",
        }
