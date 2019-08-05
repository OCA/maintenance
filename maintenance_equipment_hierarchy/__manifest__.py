# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Maintenance Equipments Hierarchy',
    'summary': 'Manage equipment hierarchy',
    'author': 'Eficent, Odoo Community Association (OCA)',
    'website': 'http://github.com/OCA/maintenance',
    'category': 'Equipments, Assets, Internal Hardware, Allocation Tracking',
    'version': '11.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'maintenance',
    ],
    'data': [
        'views/maintenance_equipment_views.xml',
    ],
    'demo': [
        'data/demo_maintenance_equipment_hierarchy.xml'
    ],
}
