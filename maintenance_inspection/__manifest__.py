# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Inspection",
    "summary": """
        Allow to manage inspections inside Preventive requests""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance_plan", "base_maintenance"],
    "data": [
        "views/maintenance_plan.xml",
        "security/ir.model.access.csv",
        "views/maintenance_inspection_line.xml",
        "views/maintenance_inspection_item.xml",
        "views/maintenance_request.xml",
    ],
    "demo": [],
}
