from odoo import api, fields, models
from odoo.tools.sql import SQL


class TimesheetsAnalysisReport(models.Model):
    _inherit = "timesheets.analysis.report"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request", readonly=True
    )

    @api.model
    def _select(self):
        return SQL(
            """%s,
            A.maintenance_request_id AS maintenance_request_id
        """,
            super()._select(),
        )

    @api.model
    def _from(self):
        return SQL(
            """%s
            LEFT JOIN maintenance_request MR ON A.maintenance_request_id = MR.id
        """,
            super()._from(),
        )
