# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    def _compute_recurring_maintenance(self):
        res = super()._compute_recurring_maintenance()
        # override Odoo's maintenance recurring field to always be False
        for request in self:
            request.recurring_maintenance = False
        return res
