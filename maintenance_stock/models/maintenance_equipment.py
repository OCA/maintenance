# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    stock_picking_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="maintenance_equipment_id",
        groups="stock.group_stock_user",
    )
    allow_consumptions = fields.Boolean(
        groups="stock.group_stock_user",
    )
    default_consumption_warehouse_id = fields.Many2one(
        string="Default Consumption Warehouse",
        comodel_name="stock.warehouse",
        groups="stock.group_stock_user",
    )

    @api.onchange("allow_consumptions")
    def _onchange_allow_consumptions(self):
        if not self.allow_consumptions:
            self.default_consumption_warehouse_id = False

    def action_view_stock_picking_ids(self):
        self.ensure_one()
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        action["domain"] = [("maintenance_equipment_id", "=", self.id)]
        action["context"] = {
            "show_maintenance_request_id": True,
        }
        return action

    def action_view_stock_move_ids(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('maintenance_equipment_id', '=', self.id)]
        return action

    def action_view_stock_move_line_ids(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        action['domain'] = [('maintenance_equipment_id', '=', self.id)]

        # TODO Grouping by destination allows separating consumptions
        #      and returns. Look for a better system and remove this
        show_groupby_to = len(self.env['stock.move.line'].search(
            [('maintenance_equipment_id', '=', self.id)]
        ).mapped('location_dest_id')) > 1

        action['context'] = {
            'search_default_done': 1,
            'search_default_groupby_location_dest_id': show_groupby_to,
            'search_default_groupby_product_id': 1,
        }
        return action
