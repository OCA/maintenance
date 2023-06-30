# Copyright 2017-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Groups",
    "summary": "Provides base access groups for the Maintenance App",
    "author": "Onestein, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "category": "Maintenance",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["maintenance"],
    "data": [
        "data/maintenance_data.xml",
        "security/maintenance_security.xml",
        "menuitems.xml",
    ],
}
