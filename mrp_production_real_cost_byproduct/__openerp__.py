# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Manufacturing Order Byproduct Real Cost",
    "version": "8.0.3.0.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_real_cost",
        "mrp_byproduct",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_production_views.xml",
    ],
}
