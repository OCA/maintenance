# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    equipment_ids = fields.Many2many("maintenance.equipment", string="Equipments")
