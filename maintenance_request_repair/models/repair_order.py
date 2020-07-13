# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RepairOrder(models.Model):

    _inherit = 'repair.order'

    maintenance_request_ids = fields.One2many(
        'maintenance.request',
        'repair_order_id',
        string="Maintenance Requests"
    )
