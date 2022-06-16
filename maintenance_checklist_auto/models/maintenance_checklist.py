# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools, _


class EquipmentChecklist(models.Model):
    _inherit = "equipment.checklist"

    equipment_id = fields.Many2one(
        "maintenance.equipment", "Equipment"
    )


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    @api.onchange('equipment_id')
    def onchange_checklist(self):
        if self.equipment_id:
            self.checklist_ids = False
            maintenance_checklist = []
            equipment_checklists = self.env['equipment.checklist'].search(
                [('equipment_id', '=', self.equipment_id.id)])
            for record in equipment_checklists:
                maintenance_checklist.append((0, 0, {
                    'checklist_id': record.id,
                }))
            self.checklist_ids = maintenance_checklist


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _create_new_request(self, date):
        super(MaintenanceEquipment, self)._create_new_request(date)
        if self.env.context.get('add_checklist', False):
            new_requests = self.env['maintenance.request'].search([
                ('equipment_id', '=', self.id),
                ('request_date', '=', date),
                ('stage_id.done', '=', False)], order='id desc', limit=1)
            if new_requests:
                maintenance_checklist = []
                for record in self.env['equipment.checklist'].search(
                        [('equipment_id', '=', self.id)]):
                    maintenance_checklist.append((0, 0, {
                        'checklist_id': record.id,
                    }))
                new_requests.write({'checklist_ids': maintenance_checklist})

    @api.model
    def _cron_generate_requests(self):
        return super(MaintenanceEquipment, self.with_context(
            add_checklist=True))._cron_generate_requests()
