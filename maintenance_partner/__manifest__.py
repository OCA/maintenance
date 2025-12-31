# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Partner",
    "summary": """Add Partner information in Maintenance Requests and equipments""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance"],
    "data": [
        "views/maintenance_equipment.xml",
        "views/maintenance_request.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
}
