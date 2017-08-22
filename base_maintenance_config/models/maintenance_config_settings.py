# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class MaintenanceSettings(models.TransientModel):
    _name = 'maintenance.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id, required=True)
