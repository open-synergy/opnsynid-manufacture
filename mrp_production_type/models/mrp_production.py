# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


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
