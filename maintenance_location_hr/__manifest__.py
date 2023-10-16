# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Location Hr",
    "summary": """
        Assign equipments to locations""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance_location", "hr_maintenance"],
    "data": [
        "views/maintenance_location.xml",
        "views/maintenance_equipment.xml",
    ],
    "demo": [],
}
