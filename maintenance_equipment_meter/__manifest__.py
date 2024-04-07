# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Meter",
    "summary": """
        Track meter for equipments""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance", "uom"],
    "data": [
        "views/maintenance_request.xml",
        "security/ir.model.access.csv",
        "views/maintenance_equipment_meter.xml",
        "views/maintenance_equipment.xml",
    ],
    "demo": [],
}
