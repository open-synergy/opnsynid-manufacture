# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def open_rm_traceability(self):
        self.ensure_one()
        quant_ids = []
        for rm in self.move_lines2.filtered(lambda r: r.state == "done"):
            quant_ids += rm.quant_ids.ids
        waction = self.env.ref("stock.quantsact").read()[0]
        waction["domain"] = [
            ("id", "in", quant_ids)
        ]
        return waction

    @api.multi
    def open_fg_traceability(self):
        self.ensure_one()
        quant_ids = []
        for rm in self.move_created_ids2.filtered(lambda r: r.state == "done"):
            quant_ids += rm.quant_ids.ids
        waction = self.env.ref("stock.quantsact").read()[0]
        waction["domain"] = [
            ("id", "in", quant_ids)
        ]
        return waction
