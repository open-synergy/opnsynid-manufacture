# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "MO Type Location Policy",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_type",
    ],
    "data": ["views/mrp_production_views.xml", "views/mrp_production_type_views.xml"],
}