# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class GroupStockMoveConsume(models.TransientModel):
    _inherit = "stock.group_move_consume"
    _description = "Group Consume Product"

    @api.model
    def _default_line_ids(self):
        _super = super(GroupStockMoveConsume, self)
        results = _super._default_line_ids()
        for result in results:
            result[2].update(
                {
                    "date_backdating": fields.Datetime.now(),
                }
            )
        return results


class StockMoveConsume(models.TransientModel):
    _inherit = "stock.move.consume"

    @api.model
    def _default_date_backdating(self):
        return fields.Datetime.now()

    date_backdating = fields.Datetime(
        string="Actual Movement Date",
        default=lambda self: self._default_date_backdating(),
    )

    @api.multi
    def do_move_consume(self):
        _super = super(StockMoveConsume, self)
        _super.do_move_consume()
        move = self.move_id
        move.write(
            {
                "date": self.date_backdating,
            }
        )
        if move.quant_ids:
            move.quant_ids.sudo().write(
                {
                    "in_date": self.date_backdating,
                }
            )
        return True
