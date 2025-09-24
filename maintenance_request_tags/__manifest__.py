# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Tags",
    "summary": """
        Adds tags to Maintenance Requests""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance"],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_request_tag.xml",
        "views/maintenance_request.xml",
    ],
}
