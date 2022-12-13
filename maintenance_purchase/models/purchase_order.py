# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
        action = self.env.ref("maintenance.hr_equipment_action")
        action_dict = action.sudo().read()[0]
        if len(items) == 1:
            res = self.env.ref("maintenance.hr_equipment_view_form", False)
            action_dict["views"] = [(res and res.id or False, "form")]
            action_dict["res_id"] = items.id
        elif items:
            action_dict["domain"] = [("purchase_id", "=", self.id)]
        else:
            action_dict = {"type": "ir.actions.act_window_close"}
        return action_dict

    def button_approve(self, force=False):
        result = super().button_approve(force=force)
        equipment_model = self.env["maintenance.equipment"]
        for order in self.filtered(lambda po: po.state in ("purchase", "done")):
            for line in order.order_line.filtered(
                lambda x: (
                    not x.equipment_ids
                    and x.product_id
                    and x.product_id.product_tmpl_id.maintenance_ok
                )
            ):
                if not line.equipment_category_id:
                    line._set_equipment_category()
                # Create equipments
                limit = int(line.product_qty) + 1
                vals = line._prepare_equipment_vals()
                equipment_ids = []
                for _i in range(1, limit):
                    equipment = equipment_model.create(vals)
                    equipment_ids.append((4, equipment.id))
                line.equipment_ids = equipment_ids
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    equipment_category_id = fields.Many2one(
        comodel_name="maintenance.equipment.category",
        string="Equipment Category",
        compute="_compute_equipment_category_id",
        store=True,
        readonly=False,
    )
    equipment_ids = fields.Many2many(
        comodel_name="maintenance.equipment",
        string="Equipments",
    )
    equipment_count = fields.Integer(compute="_compute_equipment_count")

    @api.depends("product_id")
    def _compute_equipment_category_id(self):
        for item in self:
            if (
                item.product_id.maintenance_ok
                and item.product_id.product_tmpl_id.categ_id.equipment_category_ids
            ):
                item.equipment_category_id = fields.first(
                    item.product_id.product_tmpl_id.categ_id.equipment_category_ids
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

    def _prepare_equipment_category_vals(self):
        categ = self.product_id.product_tmpl_id.categ_id
        return {"name": categ.name, "product_category_id": categ.id}

    def _set_equipment_category(self):
        if not self.equipment_category_id:
            category_model = self.env["maintenance.equipment.category"]
            category = category_model.create(self._prepare_equipment_category_vals())
            self.equipment_category_id = category.id

    def _prepare_equipment_vals(self):
        return {
            "purchase_line_id": self.id,
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "category_id": self.equipment_category_id.id,
            "assign_date": self.order_id.date_order,
            "effective_date": self.order_id.date_planned,
            "partner_id": self.order_id.partner_id.id,
            "partner_ref": self.order_id.partner_ref,
        }

    def _prepare_account_move_line(self, move=False):
        result = super()._prepare_account_move_line(move=move)
        result["equipment_ids"] = [
            (4, equipment.id) for equipment in self.equipment_ids
        ]
        return result
