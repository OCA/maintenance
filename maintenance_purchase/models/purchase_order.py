# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    equipment_count = fields.Integer(compute="_compute_equipment_count")

    def _compute_equipment_count(self):
        for item in self:
            item.equipment_count = sum(item.mapped("order_line.equipment_count"))

    def unlink(self):
        items = self.env["maintenance.equipment"].search(
            [("purchase_id", "in", self.ids)]
        )
        items.write({"purchase_line_id": False, "purchase_id": False})
        return super().unlink()

    def action_view_equipments(self):
        items = self.env["maintenance.equipment"].search(
            [("purchase_id", "=", self.id)]
        )
        action_dict = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance.hr_equipment_action"
        )
        if len(items) == 1:
            res = self.env.ref("maintenance.hr_equipment_view_form", False)
            action_dict["views"] = [(res and res.id or False, "form")]
            action_dict["res_id"] = items.id
        elif items:
            action_dict["domain"] = [("purchase_id", "=", self.id)]
        else:
            action_dict = {"type": "ir.actions.act_window_close"}
        return action_dict

    def _get_lines_to_create_equipments(self):
        return self.order_line.filtered(
            lambda x: (
                x.product_qty > len(x.equipment_ids)
                and x.product_id
                and x.equipment_category_id
            )
        )

    def button_approve(self, force=False):
        result = super().button_approve(force=force)
        self._create_equipments()
        return result

    def _create_equipments(self):
        for order in self.filtered(lambda po: po.state in ("purchase", "done")):
            for line in order._get_lines_to_create_equipments():
                line.create_equipments()


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    equipment_category_id = fields.Many2one(
        comodel_name="maintenance.equipment.category",
        string="Equipment Category",
        compute="_compute_equipment_category_id",
        store=True,
        readonly=False,
    )
    equipment_ids = fields.One2many(
        comodel_name="maintenance.equipment",
        inverse_name="purchase_line_id",
        string="Equipments",
        copy=False,
    )
    equipment_count = fields.Integer(compute="_compute_equipment_count")

    @api.depends("product_id")
    def _compute_equipment_category_id(self):
        for item in self:
            if item.product_id.product_tmpl_id.purchase_equipment_category_id:
                item.equipment_category_id = (
                    item.product_id.product_tmpl_id.purchase_equipment_category_id
                )
            else:
                item.equipment_category_id = item.equipment_category_id

    def _compute_equipment_count(self):
        data = self.env["maintenance.equipment"].read_group(
            [("purchase_line_id", "in", self.ids)],
            ["purchase_line_id"],
            ["purchase_line_id"],
        )
        mapping = {x["purchase_line_id"][0]: x["purchase_line_id_count"] for x in data}
        for item in self:
            item.equipment_count = mapping.get(item.id, 0)

    def _qty_to_create_equipments(self):
        return int(self.product_qty - len(self.equipment_ids))

    def create_equipments(self):
        self.ensure_one()
        equipment_model = self.env["maintenance.equipment"]
        equipments = equipment_model.create(
            [
                self._prepare_equipment_vals()
                for _ in range(self._qty_to_create_equipments())
            ]
        )
        self.equipment_ids = [Command.link(eq.id) for eq in equipments]
        return equipments

    def _prepare_equipment_vals(self):
        return {
            "purchase_line_id": self.id,
            "name": self.product_id.name,
            "category_id": self.equipment_category_id.id,
            "assign_date": self.order_id.date_order,
            "effective_date": self.order_id.date_planned,
            "partner_id": self.order_id.partner_id.id,
            "partner_ref": self.order_id.partner_ref,
            "company_id": self.order_id.company_id.id,
        }
