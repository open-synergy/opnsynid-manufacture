# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="mrp.production_type",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
