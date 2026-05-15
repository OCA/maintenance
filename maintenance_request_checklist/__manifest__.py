# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Maintenance Request Checklist",
    "summary": "Adds an execution checklist to maintenance requests",
    "version": "16.0.1.0.0",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["base_maintenance"],
    "maintainers": [
        "CristianoMafraJunior, marcelsavegnago",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_request_views.xml",
    ],
    "installable": True,
}
