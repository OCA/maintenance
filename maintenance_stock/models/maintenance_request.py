# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    allow_consumptions = fields.Boolean(
        related="equipment_id.allow_consumptions",
        store=True,
        groups="stock.group_stock_user",
    )
    default_consumption_warehouse_id = fields.Many2one(
        related="equipment_id.default_consumption_warehouse_id",
        groups="stock.group_stock_user",
    )
    stock_picking_ids = fields.One2many(
        string="Picking list",
        comodel_name="stock.picking",
        inverse_name="maintenance_request_id",
        groups="stock.group_stock_user",
    )

    def action_view_stock_picking_ids(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.stock_picking_action_picking_type"
        )
        action["domain"] = [("maintenance_request_id", "=", self.id)]
        cons_type = self.default_consumption_warehouse_id.cons_type_id
        action["context"] = {
            "default_picking_type_id": cons_type.id,
            "default_maintenance_request_id": self.id,
        }
        return action

    def action_view_stock_move_ids(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.stock_move_action"
        )
        action["domain"] = [("maintenance_request_id", "=", self.id)]
        return action

    def action_view_stock_move_line_ids(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock.stock_move_line_action"
        )
        action["domain"] = [("maintenance_request_id", "=", self.id)]

        # TODO Grouping by destination allows separating consumptions
        #      and returns. Look for a better system and remove this
        show_groupby_to = (
            len(
                self.env["stock.move.line"]
                .search([("maintenance_request_id", "=", self.id)])
                .mapped("location_dest_id")
            )
            > 1
        )

        action["context"] = {
            "search_default_done": 1,
            "search_default_groupby_location_dest_id": show_groupby_to,
            "search_default_groupby_product_id": 1,
        }
        return action
