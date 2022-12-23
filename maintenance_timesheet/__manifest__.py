# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Maintenance Timesheets",
    "summary": "Adds timesheets to maintenance requests",
    "author": "Odoo Community Association (OCA), Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.3.0",
    "category": "Human Resources",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["base_maintenance", "maintenance_project", "hr_timesheet"],
    "data": [
        "security/maintenance_timesheet_security.xml",
        "views/hr_timesheet_views.xml",
        "views/maintenance_request_views.xml",
        "report/maintenance_request_report.xml",
    ],
    "demo": ["data/demo_maintenance_timesheet.xml"],
    "installable": True,
}
