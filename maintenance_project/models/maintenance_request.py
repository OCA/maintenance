# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    project_id = fields.Many2one(comodel_name="project.project")
    task_id = fields.Many2one(comodel_name="project.task")

    @api.model_create_multi
    def create(self, vals_list):
        """
        We ensure for appropiate project and task for new requests,
        specially the automatically generated ones
        """
        newreqs = super().create(vals_list)
        for newreq in newreqs:
            if not newreq.project_id and newreq.equipment_id:
                newreq.project_id = newreq.equipment_id.project_id
            if not newreq.task_id and newreq.maintenance_type == "preventive":
                newreq.task_id = newreq.equipment_id.preventive_default_task_id

        return newreqs

    @api.onchange("equipment_id")
    def onchange_equipment_id(self):
        res = super().onchange_equipment_id()
        if self.equipment_id and self.equipment_id.project_id:
            self.project_id = self.equipment_id.project_id
        return res
