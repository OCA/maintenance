# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Availability",
    "summary": "Compute equipment availability from maintenance request results",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "author": "Quartile, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["maintenance"],
    "data": [
        "views/maintenance_request_views.xml",
        "views/maintenance_equipment_views.xml",
    ],
    "installable": True,
}
