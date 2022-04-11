# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Production Order Mass Balance Analysis",
    "version": "8.0.1.2.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
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
