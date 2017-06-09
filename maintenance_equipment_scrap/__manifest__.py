# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Maintenance Equipments Scrap',
    'summary': 'Enhance the functionality for Scrapping Equipments',
    'author': 'Onestein',
    'website': 'http://www.onestein.eu',
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'maintenance',
        'mail',
        'stock',
    ],
    'data': [
        'views/maintenance_equipment.xml',
        'views/stock_config_setting_views.xml',
        'wizard/scrap_equipment.xml',
        'data/maintenance_data.xml',
    ],
}
