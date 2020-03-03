# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Plan Activity",
    "summary": """
        This module allows defining in the maintenance plan activities that
        will be created once the maintenance requests are created as a
        consequence of the plan itself.""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://www.github.com/OCA/maintenance",
    "depends": ["maintenance_plan"],
    "data": ["security/ir.model.access.csv", "views/maintenance_views.xml"],
}
