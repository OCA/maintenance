# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    @api.model
    def _default_remote(self):
        return self.remote.id

    remote_id = fields.Many2one(
        "res.remote", readonly=True, default=lambda r: r._default_remote()
    )
