# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, _


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    wh_cons_loc_id = fields.Many2one(
        'stock.location',
        'Consumption Location',
        domain=[('usage', '=', 'inventory')])
    cons_type_id = fields.Many2one("stock.picking.type", "Consumption Type")

    def _create_or_update_sequences_and_picking_types(self):
        warehouse_data = \
            super()._create_or_update_sequences_and_picking_types()
        PickingType = self.env['stock.picking.type']

        # TODO when is called for an existing warehouse (e.g. during the
        #      module installation in_type_id is not accesible). Temporary
        #      solved with a hook
        if 'cons_type_id' in warehouse_data:
            PickingType.browse(warehouse_data['cons_type_id']).write({
                'return_picking_type_id':
                    warehouse_data.get('in_type_id', False),
            })
        return warehouse_data

    def _update_name_and_code(self, new_name=False, new_code=False):
        for warehouse in self:
            sequence_data = warehouse._get_sequence_values()
            warehouse.cons_type_id.sequence_id.write(
                sequence_data['cons_type_id'])

    def _get_picking_type_create_values(self, max_sequence):
        data, max_sequence_new = \
            super()._get_picking_type_create_values(max_sequence)
        return {
            **data,
            'cons_type_id': {
                'name': _('Consumption'),
                'code': 'outgoing',
                'use_create_lots': False,
                'use_existing_lots': True,
                'default_location_src_id': self.lot_stock_id.id,
                'default_location_dest_id': self.wh_cons_loc_id.id,
                'sequence': max_sequence_new,
                'barcode': self.code.replace(" ", "").upper() + "-CONS",
            }
        }, max_sequence_new + 1

    def _get_picking_type_update_values(self):
        data = super()._get_picking_type_update_values()
        return {
            **data,
            "cons_type_id": {}
        }

    def _get_sequence_values(self):
        data = super()._get_sequence_values()
        return {
            **data,
            'cons_type_id': {
                'name': self.name + ' ' + _('Sequence consumption'),
                'prefix': self.code + '/CONS/', 'padding': 5,
                'company_id': self.company_id.id,
            },
        }

    def _get_locations_values(self, vals):
        sub_locations = super()._get_locations_values(vals)
        code = vals.get('code') or self.code
        code = code.replace(' ', '').upper()
        company_id = vals.get('company_id', self.company_id.id)
        return {
            **sub_locations,
            'wh_cons_loc_id': {
                'name': _('Consumptions'),
                'usage': 'inventory',
                'barcode': self._valid_barcode(code + '-CONS', company_id)
            },
        }
