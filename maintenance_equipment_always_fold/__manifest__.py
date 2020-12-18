# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Maintenance Equipment Categories always_fold is indicate it",
    "summary": "Equipment categories will always be folded if I indicate it "
               "with an always_fold Boolean; if not, let him behave as before",
    "author": "Odoo Community Association (OCA), Solvos",
    "license": "AGPL-3",
    "version": "12.0.1.0.0",
    "category": "Equipments",
    "website": "https://github.com/OCA/maintenance",
    "depends": [
        "maintenance",
    ],
    "data": [
        'views/maintenance_views.xml',
        'demo/maintenance_demo.xml',
    ],
    "demo": [
    ],
    'installable': True,
}
