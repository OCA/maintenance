import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-maintenance",
    description="Meta package for oca-maintenance Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-account_asset_maintenance',
        'odoo10-addon-base_maintenance_config',
        'odoo10-addon-maintenance_equipment_scrap',
        'odoo10-addon-maintenance_plan',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
