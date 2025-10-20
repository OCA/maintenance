# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlan(models.Model):
    _inherit = "maintenance.plan"

    planned_activity_ids = fields.One2many(
        comodel_name="maintenance.planned.activity",
        inverse_name="maintenance_plan_id",
        string="Planned Activities",
    )
