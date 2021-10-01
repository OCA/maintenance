# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan',
 'summary': 'Extends preventive maintenance planning',
 'version': '11.0.2.3.1',
 'author': 'Camptocamp SA, Eficent, Odoo Community Association (OCA)',
 'license': 'AGPL-3',
 'category': 'Maintenance',
 'website': 'https://github.com/OCA/maintenance',
 'images': [],
 'depends': [
     'maintenance',
     ],
 'data': [
     'security/ir.model.access.csv',
     'views/maintenance_kind_views.xml',
     'views/maintenance_plan_views.xml',
     'views/maintenance_equipment_views.xml',
     ],
 'demo': [
     'data/demo_maintenance_plan.xml'
 ],
 'post_init_hook': 'post_init_hook',
 'installable': True,
 }
