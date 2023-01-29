# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Maintenance Checklist Timer",
    "version": "14.0.1.0.0",
    "summary": """
This module add timer on Maintenance Checklist and creates a timesheet entry.
    """,
    "author": "ArcheTI, Odoo Community Association (OCA)",
    "category": "Maintenance",
    "license": "AGPL-3",
    "images": [],
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance_timesheet", "maintenance_checklist"],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_request_views.xml",
        "wizard/maintenance_checklist_create_timesheet_views.xml",
    ],
    "installable": True,
}
