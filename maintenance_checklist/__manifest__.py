# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Maintenance Checklist",
    "version": "14.0.1.0.0",
    "category": "Maintenance",
    "images": ["static/description/checklist_007.PNG"],
    "author": "Oranga, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "summary": "Checklist Maintenance",
    "license": "AGPL-3",
    "depends": ["base", "maintenance"],
    "data": [
        "security/ir.model.access.csv",
        "views/report_maintenance_view.xml",
        "views/maintenance_checklist_view.xml",
    ],
    "installable": True,
    "application": True,
}
