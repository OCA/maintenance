# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    project_id = fields.Many2one(comodel_name="project.project", ondelete="restrict")
    preventive_default_task_id = fields.Many2one(
        string="Default Task", comodel_name="project.task"
    )

    def action_create_project(self):
        self.ensure_one()
        if not self.project_id:
            self.project_id = self.env["project.project"].create(
                self._prepare_project_from_equipment_values()
            )

    def _prepare_project_from_equipment_values(self):
        """
        Default project data creation hook
        """
        return {"name": self.name}
