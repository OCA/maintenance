# Copyright 2025 Trey, Kilobytes de Soluciones - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Maintenance equipment certification",
    "summary": "Add to store certifications associated with a equipment.",
    "category": "Human Resources",
    "version": "19.0.1.0.0",
    "author": "Trey (www.trey.es), Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "maintainers": ["cubells"],
    "license": "AGPL-3",
    "depends": [
        "maintenance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_equipment_certificate_views.xml",
        "views/certificate_reminder_rule_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
