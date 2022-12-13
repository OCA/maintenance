# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Purchase",
    "summary": """
        Create Equipments with purchases""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": [
        "maintenance_account",
        "purchase_stock",
    ],
    "data": [
        "views/purchase_order.xml",
        "views/maintenance_equipment.xml",
    ],
    "demo": [],
}
