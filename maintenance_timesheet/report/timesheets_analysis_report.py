from odoo import api, fields, models


class TimesheetsAnalysisReport(models.Model):
    _inherit = "timesheets.analysis.report"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request", readonly=True
    )

    @api.model
    def _select(self):
        return (
            super()._select()
            + """,
            A.maintenance_request_id AS maintenance_request_id
        """
        )

    @api.model
    def _from(self):
        return (
            super()._from()
            + """
            LEFT JOIN maintenance_request MR ON A.maintenance_request_id = MR.id
        """
        )
