# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Picking Type on MO's Stock Move",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mrp",
        "stock_production_operation",
        "base_ir_filters_active",
        "base_action_rule",
    ],
    "data": [
        "data/ir_filters_data.xml",
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
    ],
}
