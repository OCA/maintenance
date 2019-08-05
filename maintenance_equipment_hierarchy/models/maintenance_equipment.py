# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'

    parent_id = fields.Many2one('maintenance.equipment', 'Parent Equipment',
                                index=True, ondelete='cascade')
    child_ids = fields.One2many('maintenance.equipment', 'parent_id',
                                'Child Equipments')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    child_count = fields.Integer(
        compute='_compute_child_count',
        string="Number of child equipments")

    @api.depends('child_ids')
    def _compute_child_count(self):
        for equipment in self:
            equipment.child_count = len(equipment.child_ids)

    @api.constrains('parent_id')
    def _check_equipment_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error ! You cannot create a recursive '
                  'equipment hierarchy.'))
        return True

    def preview_child_list(self):
        return {
            'name': 'Child equipment of %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'res_id': self.id,
            'view_mode': 'list,form',
            'context': self.env.context,
            'domain': [('id', 'in', self.child_ids.ids)],
        }
