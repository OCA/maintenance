# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Base Maintenance",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "development_status": "Beta",
    "website": "https://github.com/OCA/maintenance",
    "category": "Maintenance",
    "license": "AGPL-3",
    "depends": ["maintenance"],
    "data": [
        "views/maintenance_team_views.xml",
        "views/maintenance_request_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/report_maintenance_request.xml",
    ],
    "installable": True,
}
