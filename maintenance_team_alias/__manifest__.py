# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
{
    "name": "Maintenance Team Alias",
    "summary": "Adds Email Alias configuration in maintenance teams",
    "version": "13.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["base_maintenance"],
    "data": ["views/maintenance_team_view_form.xml"],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
}
