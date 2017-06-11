# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    applied_cost_ids = fields.One2many(
        string="Applied Cost",
        comodel_name="mrp.production.applied_cost",
        inverse_name="mo_id",
    )

    applied_cost_summary_ids = fields.One2many(
        string="Applied Cost Summary",
        comodel_name="mrp.production.applied_cost_summary",
        inverse_name="mo_id",
    )
