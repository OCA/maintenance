# Copyright 2026 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Tier Validation",
    "summary": "Support a tier validation process for maintenance equipment",
    "version": "18.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "author": "Quartile, Odoo Community Association (OCA)",
    "maintainers": ["smorita7749"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["maintenance", "base_tier_validation"],
    "data": ["views/maintenance_equipment_views.xml"],
}
