# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Production Order Analysis",
    "version": "8.0.1.1.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_add_middle_stuff",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/mrp_production_rm_comparation_report.xml",
        "views/mrp_production_views.xml",
    ],
}
