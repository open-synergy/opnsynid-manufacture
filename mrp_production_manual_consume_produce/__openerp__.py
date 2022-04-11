# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Manufacturing Order's Manual Control to Consume and Produce",
    "version": "8.0.1.3.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_manual_close",
    ],
    "data": [
        "wizards/stock_move_consume.xml",
        "wizards/mrp_produce_finished_good_views.xml",
        "views/mrp_production_views.xml",
    ],
}
