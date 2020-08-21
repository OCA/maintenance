# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class RepairOrder(models.Model):

    _inherit = 'repair.order'

    maintenance_request_ids = fields.One2many(
        'maintenance.request',
        'repair_order_id',
        string="Maintenance Requests"
    )

    maintenance_request_count = fields.Integer(
        compute='_compute_maintenance_request_count',
        string='# Maintenances'
    )

    @api.depends('maintenance_request_ids')
    def _compute_maintenance_request_count(self):
        for repair in self:
            repair.maintenance_request_count = len(repair.maintenance_request_ids)

    def action_view_maintenance(self):
        return {
            'name': 'Child equipment of %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'res_id': self.id,
            'view_mode': 'list,form',
            'context': {
                **self.env.context,
                'default_repair_order_id': self.id,
                'repair_order_id_editable': False},
            'domain': [('id', 'in', self.maintenance_request_ids.ids)],
        }
