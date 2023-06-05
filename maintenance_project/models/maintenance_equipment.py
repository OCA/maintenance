# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    project_id = fields.Many2one(comodel_name="project.project", ondelete="restrict")
    create_project_from_equipment = fields.Boolean(default=True)
    preventive_default_task_id = fields.Many2one(
        string="Default Task", comodel_name="project.task"
    )

    @api.model_create_multi
    def create(self, vals_list):
        project_obj = self.env["project.project"]
        for values in vals_list:
            if values.get("create_project_from_equipment"):
                new_project = project_obj.create(
                    self._prepare_project_from_equipment_values(values)
                )
                values["project_id"] = new_project.id
        return super().create(vals_list)

    def _prepare_project_from_equipment_values(self, values):
        """
        Default project data creation hook
        """
        return {"name": values.get("name")}
