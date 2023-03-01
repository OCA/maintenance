# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Maintenance Account",
    "version": "14.0.1.0.2",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["maintenance_product", "account"],
    "installable": True,
    "data": [
        "views/maintenance_equipment_view.xml",
        "views/account_move_view.xml",
    ],
    "maintainers": ["victoralmau"],
}
