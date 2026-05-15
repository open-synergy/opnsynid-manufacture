import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-open-synergy-opnsynid-manufacture",
    description="Meta package for open-synergy-opnsynid-manufacture Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-mrp_production_backdating',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
