# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockMove(models.TransientModel):
    _name = "mrp.produce_finished_good"
    _description = "Produce Finished Good"

    @api.model
    def _default_product_id(self):
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_id.id

    @api.model
    def _default_uom_id(self):
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_uom.id

    @api.model
    def _default_product_qty(self):
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_uom_qty

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        readonly=True,
        default=_default_product_id,
    )
    product_qty = fields.Float(
        string="Qty. Produced",
        default=_default_product_qty,
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        default=_default_uom_id,
        readonly=True,
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )

    @api.multi
    def button_produce(self):
        self.ensure_one()
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        new_move_ids = move.action_consume(
            self.product_qty,
            restrict_lot_id=self.lot_id and self.lot_id.id or False)
        self.env["stock.move"].browse(new_move_ids).write({
            "production_id": move.production_id.id,
        })
        return True
