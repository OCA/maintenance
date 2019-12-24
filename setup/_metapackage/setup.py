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
        'odoo12-addon-maintenance_equipment_scrap',
        'odoo12-addon-maintenance_equipment_sequence',
        'odoo12-addon-maintenance_plan',
        'odoo12-addon-maintenance_project',
        'odoo12-addon-maintenance_project_plan',
        'odoo12-addon-maintenance_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
