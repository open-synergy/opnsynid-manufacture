# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Add Additional Produced Products on MO",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mrp",
    ],
    "data": [
        "wizards/mrp_add_produce_product_views.xml",
        "views/mrp_production_views.xml",
    ],
}
