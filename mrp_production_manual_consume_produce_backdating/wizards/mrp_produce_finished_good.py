# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class GroupProduceFinishedGood(models.TransientModel):
    _inherit = "mrp.group_produce_finished_good"

    @api.model
    def _default_line_ids(self):
        _super = super(GroupProduceFinishedGood, self)
        results = _super._default_line_ids()
        for result in results:
            result[2].update({"date_backdating": fields.Datetime.now()})
        return results


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
        move = self.move_id
        move.write({
            "date": self.date_backdating,
        })
        if move.quant_ids:
            move.quant_ids.sudo().write({
                "in_date": self.date_backdating,
            })
        return True
