# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def get_price_unit(self, move):
        if move.production_id:
            if move._is_byproduct():
                return move._get_byproduct_cost()
            elif move._is_main_product():
                return move.production_id.real_cost / move.product_qty
            else:
                return super(StockMove, self).get_price_unit(move)
        else:
            return super(StockMove, self).get_price_unit(move)

    @api.multi
    def _is_byproduct(self):
        self.ensure_one()
        mo = self.production_id
        if self.product_id.id in \
                mo.byproduct_cost_ids.mapped("product_id.id"):
            return True
        else:
            return False

    @api.multi
    def _is_main_product(self):
        self.ensure_one()
        mo = self.production_id
        if self.product_id.id == mo.product_id.id:
            return True
        else:
            return False

    @api.multi
    def _get_byproduct_cost(self):
        self.ensure_one()
        obj_bp = self.env["mrp.byproduct_cost_calculation"]
        criteria = [
            ("production_id", "=", self.production_id.id),
            ("product_id", "=", self.product_id.id),
        ]
        result = 0.0
        if obj_bp.search_count(criteria) > 0:
            result = obj_bp.search(criteria, limit=1)[0].byproduct_cost
        return result
