# Copyright 2017 Camptocamp SA
# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceKind(models.Model):

    _name = "maintenance.kind"
    _description = "Maintenance Kind"

    name = fields.Char("Name", required=True, translate=True)
    active = fields.Boolean("Active Kind", required=True, default=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Maintenance kind name already exists.")
    ]
