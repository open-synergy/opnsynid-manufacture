# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.TransientModel):
    _inherit = "mrp.produce_finished_good"

    @api.multi
    def button_produce(self):
        self.ensure_one()
        obj_lot = self.env["stock.production.lot"]
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        lot = self.lot_id
        code = (move.production_id.manual_production_lot or
                move.production_id.name or "")
        if not lot:
            lots = obj_lot.search([
                ("name", "=", code),
                ("product_id", "=", move.product_id.id),
            ])
            if len(lots) == 0:
                vals = {
                    "name": code,
                    "product_id": move.product_id.id,
                }
                lot = obj_lot.create(vals)
            else:
                lot = lots[0]
        new_move_ids = move.action_consume(
            self.product_qty,
            restrict_lot_id=lot and lot.id or False)
        self.env["stock.move"].browse(new_move_ids).write({
            "production_id": move.production_id.id,
        })
        return True
