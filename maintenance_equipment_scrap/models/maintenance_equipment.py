# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    equipment_scrap_template_id = fields.Many2one(
        'mail.template',
        string='Equipment Scrap Email Template',
    )

    @api.multi
    def action_perform_scrap(self):
        self.ensure_one()
        action = self.env.ref(
            'maintenance_equipment_scrap.wizard_perform_equipment_scrap_action'
        )
        result = action.read()[0]
        return result

    @api.multi
    @api.onchange('category_id')
    def onchange_category_id(self):
        for equipment in self:
            if equipment.category_id:
                equipment.equipment_scrap_template_id = \
                    equipment.category_id.equipment_scrap_template_id
            else:
                equipment.equipment_scrap_template_id = None
