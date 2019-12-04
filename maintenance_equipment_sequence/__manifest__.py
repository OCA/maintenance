# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Maintenance Equipment Sequence',
    'summary': """
        Adds sequence to maintenance equipment defined in the equipment's
        category""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Eficent Business and IT Consulting Services S.L.,'
              'Odoo Community Association (OCA)',
    'website': 'https://www.github.com/OCA/maintenance',
    'depends': [
        'maintenance'
    ],
    'data': [
        'views/maintenance_views.xml',
    ],
}
