# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MaintenanceEquipmentStatus(models.Model):
    _name = "maintenance.equipment.status"
    _description = "Maintenance Equipment Status"
    _order = "sequence"

    active = fields.Boolean(default=True)
    name = fields.Char("Name")
    note = fields.Text("Notes")
    sequence = fields.Integer(string="Sequence", default=10)
    category_ids = fields.Many2many(
        string="Categories",
        comodel_name="maintenance.equipment.category",
        help="When set, this status will only be applicable to the equipments "
        "under these categories.",
    )
