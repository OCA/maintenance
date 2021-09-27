# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    equipment_scrap_template_id = fields.Many2one(
        "mail.template",
        compute="_compute_equipment_scrap_template_id",
        store=True,
        readonly=False,
        string="Equipment Scrap Email Template",
    )

    def action_perform_scrap(self):
        self.ensure_one()
        action = self.env.ref(
            "maintenance_equipment_scrap.wizard_perform_equipment_scrap_action"
        )
        result = action.read()[0]
        return result

    @api.depends("category_id.equipment_scrap_template_id")
    def _compute_equipment_scrap_template_id(self):
        for equipment in self:
            if equipment.category_id:
                equipment.equipment_scrap_template_id = (
                    equipment.category_id.equipment_scrap_template_id
                )
            else:
                equipment.equipment_scrap_template_id = None
