# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    contract_ids = fields.Many2many(
        'account.analytic.account', string='Contracts'
    )
    contract_count = fields.Integer(
        compute='_compute_contract_count',
    )

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids.ids)

    @api.multi
    def action_view_contracts(self):
        action = self.env.ref(
            'contract.action_account_analytic_purchase_overdue_all').read()[0]
        if len(self.contract_ids) > 1:
            action['domain'] = [('id', 'in', self.contract_ids.ids)]
        elif self.contract_ids:
            action['views'] = [(self.env.ref(
                'contract.account_analytic_account_purchase_form'
            ).id, 'form')]
            action['res_id'] = self.contract_ids.id
        action['context'] = {
            'default_equipment_ids': self.ids,
            'is_contract': 1,
            'search_default_not_finished': 1,
            'search_default_recurring_invoices': 1,
            'default_recurring_invoices': 1,
            'default_contract_type': 'purchase'
        }
        return action
