# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    helpdesk_ticket_ids = fields.Many2many(
        "helpdesk.ticket",
        "maintenance_helpdesk_ticket",
        "maintenance_request_id",
        "helpdesk_ticket_id",
        string="Helpdesk Tickets",
        copy=False,
    )
