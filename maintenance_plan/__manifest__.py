# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan',
 'summary': 'Extends preventive maintenance planning',
 'version': '10.0.1.0.0',
 'author': 'Odoo Community Association (OCA), Camptocamp SA',
 'license': 'AGPL-3',
 'category': 'Maintenance',
 'website': 'http://www.camptocamp.com',
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
 'auto_install': False,
 }
