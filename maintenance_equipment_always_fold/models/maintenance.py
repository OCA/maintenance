# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    @api.depends('equipment_ids', 'always_fold')
    def _compute_fold(self):
        if self.always_fold:
            self.fold = True
        else:
            super()._compute_fold()

    always_fold = fields.Boolean(string='Always Folded in Maintenance Pipe',
                                 default=False)
