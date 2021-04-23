# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

{
    'name': 'Maintenance Equipment Category Kanban',
    'summary': """
        Sets kanban category groping by default for equipments
        """,
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Solvos,'
              'Odoo Community Association (OCA)',
    'website': 'https://www.github.com/OCA/maintenance',
    'depends': [
        'maintenance'
    ],
    'data': [
        'views/maintenance_equipment_category_views.xml',
        'views/maintenance_equipment_views.xml',
    ],
}
