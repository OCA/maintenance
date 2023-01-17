# Copyright 2021 Exo Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Image",
    "summary": """Adds images to equipment.""",
    "category": "Manufacturing/Maintenance",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Exo Software," "Odoo Community Association (OCA)",
    "maintainers": ["pedrocasi"],
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance"],
    "data": [
        "views/maintenance_equipment_views.xml",
    ],
    "installable": True,
    "application": False,
}
