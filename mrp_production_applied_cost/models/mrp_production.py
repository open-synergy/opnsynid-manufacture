# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


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

    @api.multi
    def action_compute(self, properties=None):
        result = super(MrpProduction, self).action_compute(properties)
        for mo in self:
            if mo.bom_id.applied_cost_ids:
                mo.compute_applied_cost()
        return result

    @api.multi
    def compute_applied_cost(self):
        self.ensure_one()
        self.write(self._prepare_applied_cost())

    @api.multi
    def _prepare_applied_cost(self):
        self.ensure_one()
        data = []
        uom_obj = self.env["product.uom"]
        factor = uom_obj._compute_qty(
            self.product_uom.id, self.product_qty, self.bom_id.product_uom.id
        )
        factor = factor / self.bom_id.product_qty
        for cost in self.bom_id.applied_cost_ids:
            data.append((0, 0, cost._prepare_production_applied_cost(factor)))

        return {
            "applied_cost_ids": data,
        }
