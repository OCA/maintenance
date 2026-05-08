# Copyright 2017 Camptocamp SA
# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    maintenance_kind_id = fields.Many2one(
        string="Maintenance Kind",
        comodel_name="maintenance.kind",
        ondelete="restrict",
    )
    maintenance_plan_id = fields.Many2one(
        string="Maintenance Plan",
        comodel_name="maintenance.plan",
        ondelete="restrict",
    )
