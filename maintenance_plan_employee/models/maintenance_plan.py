# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"

    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")
