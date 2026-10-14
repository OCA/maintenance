# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    def copy(self, default=None):
        default = dict(default or {})
        default.update({"scrap_date": False})
        return super().copy(default=default)

    def action_perform_scrap(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance_equipment_scrap.wizard_perform_equipment_scrap_action"
        )
        return action
