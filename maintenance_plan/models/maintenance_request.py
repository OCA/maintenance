# Copyright 2017 Camptocamp SA
# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    maintenance_kind_id = fields.Many2one(string='Maintenance kind',
                                          comodel_name='maintenance.kind',
                                          ondelete='restrict')

    maintenance_plan_id = fields.Many2one(string='Maintenance plan',
                                          comodel_name='maintenance.plan',
                                          ondelete='restrict')
    note = fields.Html('Note')
