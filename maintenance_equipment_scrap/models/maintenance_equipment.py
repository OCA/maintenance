# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    equipment_scrap_template_id = fields.Many2one(
        'mail.template',
        string='Equipment Scrap Email Template',
        default=(lambda self:
                 self.env.user.company_id.equipment_scrap_template_id)
    )

    @api.multi
    def action_perform_scrap(self):
        self.ensure_one()
        action = self.env.ref(
            'maintenance_equipment_scrap.wizard_perform_equipment_scrap_action'
        )
        result = action.read()[0]
        return result
