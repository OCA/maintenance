import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-base_maintenance',
        'odoo11-addon-base_maintenance_config',
        'odoo11-addon-base_maintenance_group',
        'odoo11-addon-maintenance_equipment_hierarchy',
        'odoo11-addon-maintenance_equipment_scrap',
        'odoo11-addon-maintenance_equipment_sequence',
        'odoo11-addon-maintenance_equipment_status',
        'odoo11-addon-maintenance_equipment_tags',
        'odoo11-addon-maintenance_plan',
        'odoo11-addon-maintenance_request_sequence',
        'odoo11-addon-maintenance_team_hierarchy',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
