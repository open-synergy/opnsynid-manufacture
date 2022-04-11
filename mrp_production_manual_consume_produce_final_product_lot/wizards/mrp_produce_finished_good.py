# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class StockMove(models.TransientModel):
    _inherit = "mrp.produce_finished_good"

    @api.multi
    def _get_lot_id(self):
        self.ensure_one()
        lot = self.lot_id
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        code = move.production_id.manual_production_lot or move.production_id.name or ""
        obj_lot = self.env["stock.production.lot"]
        if not lot:
            lots = obj_lot.search(
                [
                    ("name", "=", code),
                    ("product_id", "=", move.product_id.id),
                ]
            )
            if len(lots) == 0:
                vals = {
                    "name": code,
                    "product_id": move.product_id.id,
                }
                lot = obj_lot.create(vals)
            else:
                lot = lots[0]
        return lot and lot.id or False
