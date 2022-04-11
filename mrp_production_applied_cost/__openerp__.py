# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Manufacturing Order Applied Cost",
    "version": "8.0.2.1.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_real_cost",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_views.xml",
        "views/mrp_production_views.xml",
    ],
}
