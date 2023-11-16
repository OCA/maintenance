# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Tags",
    "summary": """
        Adds category tags to equipment""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "maintainers": ["etobella"],
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance"],
    "demo": ["demo/maintenance_equipment_tags_demo.xml"],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_equipment.xml",
        "views/maintenance_equipment_tag.xml",
    ],
    "installable": False,
}
