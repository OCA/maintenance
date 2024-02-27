# Copyright 2022-2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    usage_ids = fields.One2many(
        comodel_name="maintenance.equipment.usage",
        inverse_name="equipment_id",
        string="Usages",
    )
    usage_count = fields.Integer(compute="_compute_usage_count")
    in_use = fields.Boolean(compute="_compute_in_use", store=True)

    @api.depends("usage_ids")
    def _compute_usage_count(self):
        res = self.env["maintenance.equipment.usage"].read_group(
            domain=[("equipment_id", "in", self.ids)],
            fields=["equipment_id"],
            groupby=["equipment_id"],
        )
        res_dict = {x["equipment_id"][0]: x["equipment_id_count"] for x in res}
        for rec in self:
            rec.usage_count = res_dict.get(rec.id, 0)

    @api.depends("usage_ids", "usage_ids.state")
    def _compute_in_use(self):
        for item in self:
            item.in_use = any(usage.state == "in_use" for usage in item.usage_ids)
