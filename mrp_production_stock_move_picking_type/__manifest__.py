# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Picking Type on MO's Stock Move",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mrp",
        "stock_production_operation",
        "base_automation",
    ],
    "data": [
        "data/base_automation_data.xml",
    ],
}
