# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class MrpByproductCostCalculation(models.Model):
    _name = "mrp.byproduct_cost_calculation"
    _description = "Byproduct Cost Calculation"

    @api.multi
    def _compute_join_cost(self):
        obj_line = self.env["account.analytic.line"]
        for cost in self:
            cost.join_cost = 0.0
            criteria = [
                ("mrp_production_id", "=", cost.production_id.id),
            ]
            if cost.join_cost_method == "manual_selection":
                criteria.append(
                    ("id", "in", cost.join_cost_ids.ids))
            if cost.join_cost_method != "manual":
                for line in obj_line.search(criteria):
                    cost.join_cost += -1.0 * line.amount
            else:
                cost.join_cost = cost.manual_join_cost

    @api.multi
    def _compute_cost(self):
        for cost in self:
            cost.product_qty_result = 0.0
            if cost.byproduct_cost_alocation_method == "unit":
                # TODO: Not implemented
                cost.byproduct_cost = 0.0
            elif cost.byproduct_cost_alocation_method == "weighted":
                cost.byproduct_cost = cost.multiplier * cost.join_cost

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    product_id = fields.Many2one(
        string="Byproduct",
        comodel_name="product.product",
        required=True,
    )
    byproduct_cost_alocation_method = fields.Selection(
        string="Byproduct Cost Alocation Method",
        selection=[
            ("unit", "Unit"),
            ("weighted", "Weighted"),
        ],
        related="production_id.byproduct_cost_alocation_method",
    )
    join_cost_method = fields.Selection(
        string="Join Cost Method",
        selection=[
            ("auto", "Auto"),
            ("manual_selection", "Manual Selection"),
            ("manual", "Manual"),
        ],
        required=True,
        default="auto",
    )
    manual_join_cost = fields.Float(
        string="Join Cost",
    )
    join_cost = fields.Float(
        string="Join Cost",
        compute="_compute_join_cost",
    )
    join_cost_ids = fields.Many2many(
        strin="Join Cost Detail",
        comodel_name="account.analytic.line",
        relation="rel_manual_overhead_cost",
        column1="ovh_id",
        column2="line_id",
    )
    multiplier = fields.Float(
        string="Multiplier",
    )
    byproduct_cost = fields.Float(
        string="Byproduct Cost",
        compute="_compute_cost",
    )


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def _compute_total_bp(self):
        for mo in self:
            mo.bp_real_cost = 0.0
            for bp in mo.byproduct_cost_ids:
                mo.bp_real_cost += bp.byproduct_cost

    @api.multi
    @api.depends(
        "analytic_line_ids", "analytic_line_ids.amount",
        "product_qty", "bp_real_cost", "byproduct_cost_ids",
        "byproduct_cost_ids.byproduct_cost")
    def _compute_real_cost(self):
        for production in self:
            cost_lines = production.analytic_line_ids.filtered(
                lambda l: l.amount < 0)
            production.real_cost = - \
                sum(cost_lines.mapped('amount')) - production.bp_real_cost
            production.unit_real_cost = (
                production.real_cost / production.product_qty)

    real_cost = fields.Float(
        compute="_compute_real_cost",
    )
    unit_real_cost = fields.Float(
        compute="_compute_real_cost",
    )
    byproduct_cost_alocation_method = fields.Selection(
        string="Byproduct Cost Alocation Method",
        selection=[
            ("unit", "Unit"),
            ("weighted", "Weighted"),
        ],
        required=True,
        default="weighted",
        readonly=False,
        states={
            "done": [("readonly", True)],
            "cancel": [("readonly", True)],
        },
    )
    byproduct_cost_ids = fields.One2many(
        string="Byproduct Cost",
        comodel_name="mrp.byproduct_cost_calculation",
        inverse_name="production_id",
        readonly=False,
        states={
            "done": [("readonly", True)],
            "cancel": [("readonly", True)],
        },
    )
    bp_real_cost = fields.Float(
        string="Byproduct Real Cost",
        compute="_compute_total_bp",
    )
