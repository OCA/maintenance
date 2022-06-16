# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools, _
from odoo.addons.maintenance_checklist_auto.models.maintenance_checklist \
    import (MaintenanceEquipment as AutoMaintenanceEquipment)
from odoo.addons.maintenance_plan.models.maintenance_equipment import (
    MaintenanceEquipment as PlanMaintenanceEquipment,
)


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def _create_new_request(self, obj):
        """
        execute the method implemented in the maintenance_plan
        module and then add the implementation of the
        maintenance_checklist_auto module, without calling
        super, since the two methods receive different parameters
        """
        requests = PlanMaintenanceEquipment._create_new_request(self, obj)
        if self.env.context.get('add_checklist', False):
            for request in requests:
                maintenance_checklist = []
                for record in self.env['equipment.checklist'].search(
                        [('equipment_id', '=', request.equipment_id.id)]):
                    maintenance_checklist.append((0, 0, {
                        'checklist_id': record.id,
                    }))
                request.write({'checklist_ids': maintenance_checklist})

    @api.model
    def _cron_generate_requests(self):
        return super(AutoMaintenanceEquipment, self.with_context(
            add_checklist=True))._cron_generate_requests()
