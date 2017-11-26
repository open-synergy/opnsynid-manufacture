# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class ProduceFinishedGood(models.TransientModel):
    _inherit = "mrp.produce_finished_good"

    @api.model
    def _default_date_backdating(self):
        return fields.Datetime.now()

    date_backdating = fields.Datetime(
        string="Actual Movement Date",
        default=lambda self: self._default_date_backdating(),
        )

    @api.multi
    def button_produce(self):
        self.ensure_one()
        _super = super(ProduceFinishedGood, self)
        _super.button_produce()
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        move.write({
            "date": self.date_backdating,
            })
        if move.quant_ids:
            move.quant_ids.sudo().write({
                "in_date": self.date_backdating,
                })
        return True
