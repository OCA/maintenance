# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Purchase",
    "summary": """
        Allows you to link PO with maintenance requests""",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "author": "CreuBlanca,Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["base_maintenance", "purchase"],
    "data": [
        "views/maintenance_request.xml",
        "views/purchase_order_views.xml",
    ],
}
