# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    equipment_count = fields.Integer(compute="_compute_equipment_count")

    def _compute_equipment_count(self):
        for item in self:
            item.equipment_count = sum(item.mapped("line_ids.equipment_count"))

    def unlink(self):
        items = self.env["maintenance.equipment"].search([("move_id", "in", self.ids)])
        items.write({"move_line_id": False, "move_id": False})
        return super().unlink()

    def action_post(self):
        super().action_post()
        # Prevent error if user does not have permission to create equipments
        equipment_model = self.env["maintenance.equipment"].sudo()
        for move in self.filtered(lambda r: r.is_purchase_document()):
            for line in move.line_ids.filtered(
                lambda x: (
                    not x.equipment_ids
                    and x.product_id
                    and x.product_id.product_tmpl_id.maintenance_ok
                )
            ):
                if not line.equipment_category_id:
                    line._set_equipment_category()
                # Create equipments
                limit = int(line.quantity) + 1
                vals = line._prepare_equipment_vals()
                equipment_ids = []
                for _i in range(1, limit):
                    equipment = equipment_model.with_company(
                        move.company_id,
                    ).create(vals.copy())
                    equipment_ids.append((4, equipment.id))
                line.equipment_ids = equipment_ids

    def action_view_equipments(self):
        items = self.env["maintenance.equipment"].search([("move_id", "=", self.id)])
        action = self.env.ref("maintenance.hr_equipment_action")
        action_dict = action.sudo().read()[0]
        if len(items) == 1:
            res = self.env.ref("maintenance.hr_equipment_view_form", False)
            action_dict["views"] = [(res and res.id or False, "form")]
            action_dict["res_id"] = items.id
        elif items:
            action_dict["domain"] = [("id", "in", items.ids)]
        else:
            action_dict = {"type": "ir.actions.act_window_close"}
        return action_dict


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

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
            [("move_line_id", "in", self.ids)], ["move_line_id"], ["move_line_id"]
        )
        mapping = {x["move_line_id"][0]: x["move_line_id_count"] for x in data}
        for item in self:
            item.equipment_count = mapping.get(item.id, 0)

    def _prepare_equipment_category_vals(self):
        categ = self.product_id.product_tmpl_id.categ_id
        return {"name": categ.name, "product_category_id": categ.id}

    def _set_equipment_category(self):
        if not self.equipment_category_id:
            # Prevent error if user does not have permission to create equipments
            category_model = self.env["maintenance.equipment.category"].sudo()
            category = category_model.with_company(self.company_id).create(
                self._prepare_equipment_category_vals()
            )
            self.equipment_category_id = category.id

    def _prepare_equipment_vals(self):
        return {
            "move_line_id": self.id,
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "category_id": self.equipment_category_id.id,
            "assign_date": self.move_id.date,
            "effective_date": self.move_id.date,
            "partner_id": self.move_id.partner_id.id,
            "partner_ref": self.move_id.ref,
        }
