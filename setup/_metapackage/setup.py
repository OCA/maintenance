import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-base_maintenance',
        'odoo14-addon-base_maintenance_config',
        'odoo14-addon-base_maintenance_group',
        'odoo14-addon-maintenance_equipment_contract',
        'odoo14-addon-maintenance_equipment_hierarchy',
        'odoo14-addon-maintenance_equipment_scrap',
        'odoo14-addon-maintenance_equipment_sequence',
        'odoo14-addon-maintenance_equipment_status',
        'odoo14-addon-maintenance_equipment_tags',
        'odoo14-addon-maintenance_plan',
        'odoo14-addon-maintenance_plan_activity',
        'odoo14-addon-maintenance_project',
        'odoo14-addon-maintenance_project_plan',
        'odoo14-addon-maintenance_remote',
        'odoo14-addon-maintenance_request_sequence',
        'odoo14-addon-maintenance_request_stage_transition',
        'odoo14-addon-maintenance_team_hierarchy',
        'odoo14-addon-maintenance_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
