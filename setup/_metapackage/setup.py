import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-base_maintenance',
        'odoo13-addon-maintenance_equipment_contract',
        'odoo13-addon-maintenance_equipment_hierarchy',
        'odoo13-addon-maintenance_equipment_scrap',
        'odoo13-addon-maintenance_equipment_sequence',
        'odoo13-addon-maintenance_equipment_status',
        'odoo13-addon-maintenance_equipment_tags',
        'odoo13-addon-maintenance_plan',
        'odoo13-addon-maintenance_plan_activity',
        'odoo13-addon-maintenance_project',
        'odoo13-addon-maintenance_project_plan',
        'odoo13-addon-maintenance_request_sequence',
        'odoo13-addon-maintenance_request_stage_transition',
        'odoo13-addon-maintenance_team_hierarchy',
        'odoo13-addon-maintenance_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
