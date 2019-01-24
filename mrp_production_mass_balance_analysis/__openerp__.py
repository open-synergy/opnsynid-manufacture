# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Production Order Mass Balance Analysis",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "product_multiple_uom_conversion",
        "mrp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/mrp_production_mass_balance_analysis.xml",
        "views/res_company_views.xml",
    ],
}
