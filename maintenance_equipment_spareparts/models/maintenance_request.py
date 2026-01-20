# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    sparepart_ids = fields.Many2many(
        comodel_name="maintenance.equipment.sparepart",
        string="Equipment Spare Parts",
        compute="_compute_sparepart_ids",
        readonly=True,
    )

    @api.depends("equipment_id", "equipment_id.sparepart_ids")
    def _compute_sparepart_ids(self):
        for record in self:
            if record.equipment_id:
                record.sparepart_ids = record.equipment_id.sparepart_ids
            else:
                record.sparepart_ids = False

    def action_consume_spareparts(self):
        self.ensure_one()
        if not self.equipment_id:
            raise UserError(_("Equipment must be set to consume spare parts."))
        return {
            "name": _("Consume Spare Parts"),
            "type": "ir.actions.act_window",
            "res_model": "maintenance.request.consume.spareparts",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_request_id": self.id,
            },
        }

    def _create_stock_picking_for_sparepart(self, sparepart, qty):
        """Create stock picking for consumption of spare part."""
        self.ensure_one()
        if not self.default_consumption_warehouse_id:
            raise UserError(
                _(
                    "Default consumption warehouse must be set on equipment "
                    "to consume spare parts from stock."
                )
            )
        warehouse = self.default_consumption_warehouse_id
        cons_type = warehouse.cons_type_id
        if not cons_type:
            raise UserError(
                _("Consumption picking type must be configured on warehouse %s.")
                % warehouse.display_name
            )
        picking_vals = {
            "picking_type_id": cons_type.id,
            "location_id": cons_type.default_location_src_id.id,
            "location_dest_id": cons_type.default_location_dest_id.id,
            "maintenance_request_id": self.id,
            "maintenance_equipment_id": self.equipment_id.id,
            "origin": _("Maintenance Request %s") % self.name,
        }
        picking = self.env["stock.picking"].create(picking_vals)
        move_vals = {
            "name": sparepart.product_id.display_name,
            "product_id": sparepart.product_id.id,
            "product_uom": sparepart.product_id.uom_id.id,
            "product_uom_qty": qty,
            "picking_id": picking.id,
            "location_id": picking.location_id.id,
            "location_dest_id": picking.location_dest_id.id,
        }
        move = self.env["stock.move"].create(move_vals)
        move._action_confirm()
        picking._autoconfirm_picking()
        return picking

    def _create_purchase_request_for_sparepart(self, sparepart, qty):
        """Create purchase request for spare part not in stock."""
        self.ensure_one()
        # Find or create purchase request
        purchase_request = self.env["purchase.request"].search(
            [
                ("origin", "=", self.name),
                ("state", "in", ["draft", "to_approve"]),
                ("company_id", "=", self.company_id.id),
            ],
            limit=1,
        )
        if not purchase_request:
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
                    "origin": self.name,
                    "requested_by": self.env.user.id,
                    "company_id": self.company_id.id,
                    "picking_type_id": picking_type.id if picking_type else False,
                    "equipment_id": self.equipment_id.id,
                }
            )
        line_vals = {
            "request_id": purchase_request.id,
            "product_id": sparepart.product_id.id,
            "product_uom_id": sparepart.product_id.uom_id.id,
            "product_qty": qty,
            "name": sparepart.product_id.display_name,
        }
        line = self.env["purchase.request.line"].create(line_vals)
        return purchase_request, line
