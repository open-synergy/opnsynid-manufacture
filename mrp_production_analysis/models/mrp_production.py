# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    rm_plan_summary_ids = fields.One2many(
        string="RM Plan Summary",
        comodel_name="mrp.production_rm_plan_summary",
        inverse_name="production_id",
    )
    rm_realization_summary_ids = fields.One2many(
        string="RM Realization Summary",
        comodel_name="mrp.production_rm_realization_summary",
        inverse_name="production_id",
    )
    rm_analysis_ids = fields.One2many(
        string="RM Analysis",
        comodel_name="mrp.production_rm_analysis",
        inverse_name="production_id",
    )
