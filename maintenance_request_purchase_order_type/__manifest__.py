# Copyright 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Maintenance Request Purchase",
    "summary": """
        Link PO with maintenance requests - Order Type configuration""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Solvos",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance_request_purchase", "purchase_order_type"],
    "data": [
        "views/maintenance_request_views.xml",
        "views/purchase_order_type_views.xml",
    ],
}
