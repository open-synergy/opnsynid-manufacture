# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    applied_cost_ids = fields.One2many(
        string="Applied Costs",
        comodel_name="mrp.bom.applied_cost",
        inverse_name="bom_id",
    )
