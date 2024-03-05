import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_maintenance>=16.0dev,<16.1dev',
        'odoo-addon-base_maintenance_group>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_account>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_contract>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_hierarchy>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_image>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_sequence>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_status>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_tags>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_equipment_usage>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_plan>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_product>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_project>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_request_repair>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_request_sequence>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_request_stage_transition>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_security>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_team_hierarchy>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_timesheet>=16.0dev,<16.1dev',
        'odoo-addon-maintenance_timesheet_time_control>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
