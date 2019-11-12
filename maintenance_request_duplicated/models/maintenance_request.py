# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    parent_id = fields.Many2one(
        'maintenance.request', 'Same as',
        index=True, ondelete='cascade',
        readonly=True,
    )
    child_ids = fields.One2many(
        'maintenance.request',
        inverse_name='parent_id',
        string='Duplicated Requests',
        readonly=True,
    )

    @api.multi
    def deduplicate(self):
        self.ensure_one()
        self.write({'parent_id': False})
