# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Maintenance Stock",
    "summary": "Links maintenance requests to stock",
    "author": "Odoo Community Association (OCA), Solvos",
    "license": "AGPL-3",
    "version": "12.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/OCA/maintenance",
    "depends": [
        "base_maintenance",
        "stock",
    ],
    "data": [
        "views/maintenance_equipment_views.xml",
        "views/maintenance_request_views.xml",
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
    ],
    "demo": [
        "data/demo_maintenance_stock.xml",
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
}
