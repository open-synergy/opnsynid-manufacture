# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Backdating on Manufacturing Order",
    "version": "8.0.1.1.0",
    "category": "Manufacturing",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "mrp_production_manual_consume_produce",
        "stock_move_backdating",
    ],
    "data": [
        "wizards/mrp_produce_finished_good_views.xml",
        "wizards/stock_move_consume_views.xml",
    ],
}
