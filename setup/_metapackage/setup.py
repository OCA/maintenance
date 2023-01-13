import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_maintenance>=15.0dev,<15.1dev',
        'odoo-addon-base_maintenance_config>=15.0dev,<15.1dev',
        'odoo-addon-base_maintenance_group>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_contract>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_hierarchy>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_scrap>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_sequence>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_status>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_equipment_tags>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_plan>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_plan_activity>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_product>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_project>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_remote>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_request_sequence>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_request_stage_transition>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_team_hierarchy>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_timesheet>=15.0dev,<15.1dev',
        'odoo-addon-maintenance_timesheet_time_control>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
