# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': "Maintenance Equipment Custom Info",
    'summary': "Add custom info in equipments",
    'author': 'Odoo Community Association (OCA), Solvos',
    'website': 'https://github.com/OCA/maintenance',
    'category': 'Maintenance',
    'version': '12.0.2.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base_custom_info',
        'maintenance',
    ],
    'data': [
        'security/maintenance_equipment_custom_info_security.xml',
        'views/maintenance_equipment_views.xml',
    ],
    'demo': [
        'demo/custom.info.category.csv',
        'demo/custom.info.template.csv',
        'demo/custom.info.property.csv',
        'demo/custom.info.option.csv',
        'demo/res_groups.xml',
        'demo/defaults.xml',
    ],
    'installable': True,
}
