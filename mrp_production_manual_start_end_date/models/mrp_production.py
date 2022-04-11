# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    manual_date_start = fields.Datetime(
        string="Manual Start Date",
        states={
            "done": [
                ("readonly", True),
            ],
            "cancel": [
                ("readonly", True),
            ],
        },
    )
    manual_date_finished = fields.Datetime(
        string="Manual End Date",
        states={
            "done": [
                ("readonly", True),
            ],
            "cancel": [
                ("readonly", True),
            ],
        },
    )
