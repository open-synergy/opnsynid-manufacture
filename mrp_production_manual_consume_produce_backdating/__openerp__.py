# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Backdating on Manufacturing Order",
    "version": "8.0.1.1.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
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
