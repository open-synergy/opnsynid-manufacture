# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def _get_production_rm_type(self):
        self.ensure_one()

        obj_location = self.env["stock.location"]
        obj_wh = self.env["stock.warehouse"]
        loc = self.location_src_id
        wh_id = obj_location.get_warehouse(loc)

        if not wh_id:
            return True

        wh = obj_wh.browse([wh_id])[0]

        if not wh.production_rm_type_id:
            return True

        return wh.production_rm_type_id

    @api.multi
    def _get_production_fg_type(self):
        self.ensure_one()

        obj_location = self.env["stock.location"]
        obj_wh = self.env["stock.warehouse"]
        loc = self.location_dest_id
        wh_id = obj_location.get_warehouse(loc)

        if not wh_id:
            return True

        wh = obj_wh.browse([wh_id])[0]

        if not wh.production_fg_type_id:
            return True

        return wh.production_fg_type_id
