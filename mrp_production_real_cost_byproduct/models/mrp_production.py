# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class MrpByproductCostCalculation(models.Model):
    _name = "mrp.byproduct_cost_calculation"
    _description = "Byproduct Cost Calculation"

    @api.multi
    @api.depends(
        "join_cost_method",
        "join_cost_ids",
        "join_cost_ids.amount",
        "join_cost_ids.unit_amount",
        "compute_unit_price_from",
        "manual_join_cost",
        "production_id",
    )
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
                    if cost.compute_unit_price_from == "total":
                        cost.join_cost += -1.0 * line.amount
                    else:
                        cost.join_cost += -1.0 * \
                            (line.amount / line.unit_amount)
            else:
                cost.join_cost = cost.manual_join_cost

    @api.multi
    def _compute_cost(self):
        for cost in self:
            obj_move = self.env["stock.move"]
            qty_produced = 0.0
            byproduct_cost = 0.0
            byproduct_subtotal = 0.0
            criteria = [
                ("product_id", "=", cost.product_id.id),
                ("state", "=", "done"),
                ("production_id", "=", cost.production_id.id),
            ]
            produced_stock_moves = obj_move.search(
                criteria)
            if len(produced_stock_moves) > 0:
                cost.produced_stock_move_ids = produced_stock_moves.ids
            for move in produced_stock_moves:
                qty_produced += move.product_qty

            cost.qty_produced = qty_produced

            cost.product_qty_result = 0.0
            if cost.byproduct_cost_alocation_method == "unit":
                # TODO: Not implemented
                cost.byproduct_cost = 0.0
            elif cost.byproduct_cost_alocation_method == "weighted":
                byproduct_cost = cost.multiplier * cost.join_cost
                byproduct_subtotal = byproduct_cost * qty_produced
            cost.byproduct_cost = byproduct_cost
            cost.byproduct_subtotal = byproduct_subtotal

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
    compute_unit_price_from = fields.Selection(
        string="Compute Unit Price From",
        selection=[
            ("total", "Total"),
            ("unit_price", "Unit Price"),
        ],
        required=True,
        default="total",
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
    byproduct_subtotal = fields.Float(
        string="Byproduct Cost",
        compute="_compute_cost",
    )
    produced_stock_move_ids = fields.Many2many(
        string="Produced",
        comodel_name="stock.move",
        compute="_compute_cost",
    )
    qty_produced = fields.Float(
        string="Qty. Produced",
        compute="_compute_cost",
    )

    _sql_constraints = [
        ("product_unique", "unique(product_id, production_id)",
            "No same products"),
    ]


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def _compute_total_bp(self):
        for mo in self:
            mo.bp_real_cost = 0.0
            for bp in mo.byproduct_cost_ids:
                mo.bp_real_cost += bp.byproduct_subtotal

    @api.multi
    @api.depends(
        "analytic_line_ids", "analytic_line_ids.amount",
        "product_qty", "bp_real_cost", "byproduct_cost_ids",
        "byproduct_cost_ids.byproduct_cost", "move_created_ids2")
    def _compute_real_cost(self):
        for production in self:
            obj_move = self.env["stock.move"]
            criteria = [
                ("production_id", "=", production.id),
                ("product_id", "=", production.product_id.id),
                ("state", "=", "done"),
            ]
            qty_produced = 0.0
            for move in obj_move.search(criteria):
                qty_produced += move.product_qty
            cost_lines = production.analytic_line_ids.filtered(
                lambda l: l.amount < 0)
            production.real_cost = - \
                sum(cost_lines.mapped('amount')) - production.bp_real_cost
            if qty_produced == 0:
                production.unit_real_cost = 0
            else:
                production.unit_real_cost = (
                    production.real_cost / qty_produced)

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

    @api.multi
    def bom_id_change(self, bom_id):
        result = super(MrpProduction, self).bom_id_change(bom_id)
        obj_bom = self.env["mrp.bom"]
        byproducts = []

        if bom_id:
            bom = obj_bom.browse([bom_id])[0]

            if bom.sub_products:
                for product in bom.sub_products:
                    res = {
                        "product_id": product.product_id.id,
                        "join_cost_method": "auto",
                    }
                    byproducts.append((0, 0, res))

        result["value"].update({"byproduct_cost_ids": byproducts})
        return result
