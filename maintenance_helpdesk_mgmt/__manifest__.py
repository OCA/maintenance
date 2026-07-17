# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Helpdesk Ticket",
    "summary": """
        Allows you to link Helpdesk Tickets with maintenance requests""",
    "version": "18.0.1.1.1",
    "license": "AGPL-3",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance", "helpdesk_mgmt"],
    "data": [
        "views/maintenance_request.xml",
        "views/helpdesk_ticket_views.xml",
    ],
}
