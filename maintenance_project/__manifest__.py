# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Maintenance Projects",
    "summary": "Adds projects to maintenance equipments and requests",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA), Solvos",
    "license": "AGPL-3",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["base_maintenance", "project"],
    "data": [
        "security/maintenance_project_security.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/project_project_views.xml",
        "report/maintenance_request_report.xml",
    ],
    "demo": ["data/demo_maintenance_project.xml"],
    "installable": True,
}
