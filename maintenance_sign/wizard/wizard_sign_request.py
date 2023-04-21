# Copyright 2023 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models


class WizardSignRequest(models.TransientModel):
    _inherit = "wizard.sign.request"

    def _prepare_line_vals(self, record):
        res = super()._prepare_line_vals(record)
        if record._name == "maintenance.equipment" and record.owner_user_id:
            res.update({"partner_id": record.owner_user_id.partner_id.id})
        return res


class WizardSignRequestLine(models.TransientModel):
    _inherit = "wizard.sign.request.line"

    def _prepare_sign_request_vals(self):
        res = super()._prepare_sign_request_vals()
        if self.record_ref._name == "maintenance.equipment":
            res.update({"maintenance_equipment_id": self.record_ref.id})
        return res
