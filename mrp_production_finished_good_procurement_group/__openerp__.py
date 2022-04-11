# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Create Procurement Group On Manufacturing Order's Finished Good",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_raw_material_procurement_group",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
}
