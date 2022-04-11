# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class AddProduceProduct(models.TransientModel):
    _inherit = "mrp.add_produce_product"

    @api.multi
    def _get_proc_group_id(self):
        self.ensure_one()
        group_id = super(AddProduceProduct, self)._get_proc_group_id()
        production_id = self.env.context.get("active_id", False)
        production = self.env["mrp.production"].browse([production_id])[0]
        if production.fg_procurement_group_id:
            return production.fg_procurement_group_id.id
        else:
            return group_id
