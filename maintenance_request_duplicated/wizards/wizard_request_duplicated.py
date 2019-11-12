# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WizardRequestDuplicated(models.TransientModel):

    _name = 'wizard.request.duplicated'

    duplicated_request = fields.Many2one(
        comodel_name='maintenance.request'
    )
    original_request = fields.Many2one(
        comodel_name='maintenance.request', required=True,
    )

    @api.multi
    def mark_as_duplicated(self):
        self.ensure_one()
        if not self.duplicated_request:
            raise ValidationError(_('Active Request not found'))

        self.original_request.write({
            'child_ids': [(4, self.duplicated_request.id)]
        })
        self.duplicated_request.write({
            'stage_id': self.original_request.stage_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}
