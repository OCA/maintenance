# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Location",
    "summary": """
        Define a location system for maintenance""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance_plan"],
    "data": [
        "views/maintenance_plan.xml",
        "views/maintenance_equipment.xml",
        "security/ir.model.access.csv",
        "views/maintenance_request.xml",
        "views/maintenance_location.xml",
    ],
}
