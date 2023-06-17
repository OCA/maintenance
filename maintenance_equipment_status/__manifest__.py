# Copyright 2020 ForgeFlow S.L. (https://forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Maintenance Equipment Status",
    "version": "16.0.1.0.0",
    "category": "",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "license": "LGPL-3",
    "depends": ["base_maintenance"],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_equipment_status_views.xml",
        "views/maintenance_equipment_views.xml",
    ],
    "demo": ["data/demo_maintenance_equipment_status.xml"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
