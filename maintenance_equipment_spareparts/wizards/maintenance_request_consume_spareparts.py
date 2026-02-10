# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MaintenanceRequestConsumeSpareparts(models.TransientModel):
    _name = "maintenance.request.consume.spareparts"
    _description = "Consume Spare Parts Wizard"

    request_id = fields.Many2one(
        comodel_name="maintenance.request",
        string="Maintenance Request",
        required=True,
        readonly=True,
    )
    line_ids = fields.One2many(
        comodel_name="maintenance.request.consume.spareparts.line",
        inverse_name="wizard_id",
        string="Lines",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        request_id = self.env.context.get("default_request_id") or res.get("request_id")
        if request_id:
            request = self.env["maintenance.request"].browse(request_id)
            if not request.equipment_id:
                raise UserError(_("Equipment must be set on the maintenance request."))
            if "line_ids" in fields_list:
                spareparts = request.equipment_id.sparepart_ids.filtered("active")
                if not spareparts:
                    raise UserError(
                        _(
                            "No spare parts are registered for equipment %s. "
                            "Please add spare parts to the equipment first."
                        )
                        % request.equipment_id.display_name
                    )
                lines = []
                for sparepart in spareparts:
                    lines.append(
                        (
                            0,
                            0,
                            {
                                "sparepart_id": sparepart.id,
                                "requested_qty": 0.0,
                            },
                        )
                    )
                if lines:
                    res["line_ids"] = lines
        return res

    def action_consume(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(
                _(
                    "No spare parts to consume. "
                    "Please add at least one line with quantity > 0."
                )
            )
        negative_lines = self.line_ids.filtered(lambda line: line.requested_qty < 0)
        if negative_lines:
            raise UserError(_("Requested quantity must be greater than or equal to 0."))
        lines_with_qty = self.line_ids.filtered(lambda line: line.requested_qty > 0)
        if not lines_with_qty:
            raise UserError(
                _(
                    "Please specify quantities to consume "
                    "(at least one line with quantity > 0)."
                )
            )

        pickings = self.env["stock.picking"]
        purchase_requests = self.env["purchase.request"]

        for line in self.line_ids:
            if line.requested_qty <= 0:
                continue
            sparepart = line.sparepart_id
            available_qty = sparepart.available_qty
            requested_qty = line.requested_qty

            if available_qty >= requested_qty:
                # Create stock picking - consume all from stock
                picking = self.request_id._create_stock_picking_for_sparepart(
                    sparepart, requested_qty
                )
                pickings |= picking
            elif available_qty > 0:
                # Partial stock: consume what's available and create PR for rest
                picking = self.request_id._create_stock_picking_for_sparepart(
                    sparepart, available_qty
                )
                pickings |= picking
                # Create purchase request for remaining quantity
                remaining_qty = requested_qty - available_qty
                purchase_request, _purchase_line = (
                    self.request_id._create_purchase_request_for_sparepart(
                        sparepart, remaining_qty
                    )
                )
                purchase_requests |= purchase_request
            else:
                # No stock available - create purchase request for all
                purchase_request, _purchase_line = (
                    self.request_id._create_purchase_request_for_sparepart(
                        sparepart, requested_qty
                    )
                )
                purchase_requests |= purchase_request

        # Return action to open the created document
        # Priority: pickings first, then purchase requests
        if pickings:
            # If multiple pickings, open the first one
            picking = pickings[0]
            return {
                "name": _("Stock Picking"),
                "type": "ir.actions.act_window",
                "res_model": "stock.picking",
                "view_mode": "form",
                "res_id": picking.id,
                "target": "current",
            }
        elif purchase_requests:
            # If multiple purchase requests, open the first one
            purchase_request = purchase_requests[0]
            return {
                "name": _("Purchase Request"),
                "type": "ir.actions.act_window",
                "res_model": "purchase.request",
                "view_mode": "form",
                "res_id": purchase_request.id,
                "target": "current",
            }
        else:
            # Should not happen, but just in case
            return {"type": "ir.actions.act_window_close"}


class MaintenanceRequestConsumeSparepartsLine(models.TransientModel):
    _name = "maintenance.request.consume.spareparts.line"
    _description = "Consume Spare Parts Wizard Line"

    wizard_id = fields.Many2one(
        comodel_name="maintenance.request.consume.spareparts",
        string="Wizard",
        required=True,
        ondelete="cascade",
    )
    sparepart_id = fields.Many2one(
        comodel_name="maintenance.equipment.sparepart",
        string="Spare Part",
        required=True,
        readonly=True,
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        related="sparepart_id.product_id",
        readonly=True,
    )
    installed_qty = fields.Float(
        string="Installed Quantity",
        compute="_compute_installed_qty",
        readonly=True,
        store=False,
        help="Quantity of this part installed in the equipment",
    )
    available_qty = fields.Float(
        string="Available Quantity",
        compute="_compute_available_qty",
        readonly=True,
        store=False,
        help="Available quantity in stock",
    )
    requested_qty = fields.Float(
        string="Quantity to Consume",
        required=True,
        default=0.0,
        help="Quantity to consume from stock or request for purchase",
    )

    @api.depends("sparepart_id", "sparepart_id.installed_qty")
    def _compute_installed_qty(self):
        for line in self:
            if line.sparepart_id:
                line.installed_qty = line.sparepart_id.installed_qty
            else:
                line.installed_qty = 0.0

    @api.depends("sparepart_id", "sparepart_id.available_qty")
    def _compute_available_qty(self):
        for line in self:
            if line.sparepart_id:
                line.available_qty = line.sparepart_id.available_qty
            else:
                line.available_qty = 0.0
