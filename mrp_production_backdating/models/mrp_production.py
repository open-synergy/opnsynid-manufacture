# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    backdate = fields.Datetime(
        string="Backdate",
    )

    @api.multi
    def post_inventory(self):
        _super = super(MrpProduction, self)
        res = _super.post_inventory()
        for document in self:
            moves_raw_ids = document.move_raw_ids
            moves_to_do = \
                moves_raw_ids.filtered(
                    lambda x: x.state not in ('done', 'cancel'))
            for move_to_do in moves_to_do.filtered(lambda m: m.product_qty == 0.0 and m.quantity_done > 0):
                move_to_do.date_backdating = document.backdate
            move_finished_ids = document.move_finished_ids
            moves_to_finish = \
                move_finished_ids.filtered(
                    lambda x: x.state not in ('done','cancel'))
            for move_finish in moves_to_finish:
                move_finish.date_backdating = document.backdate
            moves_to_finish._action_done()
        return res
