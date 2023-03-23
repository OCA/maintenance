# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan',
 'summary': 'Extends preventive maintenance planning',
 'version': '12.0.1.1.0',
 'author': 'Odoo Community Association (OCA), Camptocamp SA',
 'license': 'AGPL-3',
 'category': 'Maintenance',
 'website': 'https://github.com/OCA/maintenance',
 'images': [],
 'depends': [
     'maintenance',
     ],
 'data': [
     'security/ir.model.access.csv',
     'views/maintenance.xml'
     ],
 'demo': [
     'data/demo_maintenance_plan.xml'
 ],
 'post_init_hook': 'post_init_hook',
 'installable': True,
 }
