# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Manufacturing Order Byproduct Real Cost",
    "version": "8.0.3.0.1",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
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
