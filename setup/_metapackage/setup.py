import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-base_maintenance',
        'odoo12-addon-base_maintenance_group',
        'odoo12-addon-maintenance_equipment_contract',
        'odoo12-addon-maintenance_equipment_custom_info',
        'odoo12-addon-maintenance_equipment_hierarchy',
        'odoo12-addon-maintenance_equipment_scrap',
        'odoo12-addon-maintenance_equipment_sequence',
        'odoo12-addon-maintenance_equipment_status',
        'odoo12-addon-maintenance_equipment_tags',
        'odoo12-addon-maintenance_plan',
        'odoo12-addon-maintenance_plan_activity',
        'odoo12-addon-maintenance_project',
        'odoo12-addon-maintenance_project_plan',
        'odoo12-addon-maintenance_remote',
        'odoo12-addon-maintenance_request_repair',
        'odoo12-addon-maintenance_request_sequence',
        'odoo12-addon-maintenance_request_stage_transition',
        'odoo12-addon-maintenance_stock',
        'odoo12-addon-maintenance_team_hierarchy',
        'odoo12-addon-maintenance_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
