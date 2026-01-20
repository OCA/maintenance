# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Maintenance Equipment Spare Parts",
    "summary": "Manage spare parts for maintenance equipment with "
    "purchase requisition integration",
    "version": "18.0.1.0.0",
    "category": "Maintenance",
    "website": "https://github.com/OCA/maintenance",
    "author": "KMEE, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base_maintenance",
        "maintenance_product",
        "maintenance_stock",
        "purchase_request",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/maintenance_equipment_sparepart_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_sparepart_consumption_views.xml",
        "views/maintenance_request_views.xml",
        "views/purchase_request_views.xml",
        "wizards/maintenance_request_consume_spareparts_wizard.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}
