# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def _get_production_rm_type(self):
        self.ensure_one()
        loc = self.location_src_id
        wh_id = loc.get_warehouse()
        if not wh_id:
            return True
        if not wh_id.production_rm_type_id:
            return True
        return wh_id.production_rm_type_id

    @api.multi
    def _get_production_fg_type(self):
        self.ensure_one()
        loc = self.location_dest_id
        wh_id = loc.get_warehouse()
        if not wh_id:
            return True
        if not wh_id.production_fg_type_id:
            return True
        return wh_id.production_fg_type_id
