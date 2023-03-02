# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Maintenance Plan Employee",
    "version": "13.0.1.1.0",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["maintenance_request_employee", "maintenance_plan"],
    "data": [
        "views/maintenance_plan_views.xml",
        "views/report_maintenance_request.xml",
    ],
    "installable": True,
    "maintainers": ["victoralmau"],
}
