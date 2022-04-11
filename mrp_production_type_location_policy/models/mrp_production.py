# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.onchange("type_id")
    def onchange_location_src_id(self):
        self.location_src_id = False
        if self.type_id:
            self.location_src_id = self.type_id.default_raw_material_location_id.id

    @api.onchange("type_id")
    def onchange_location_dest_id(self):
        self.location_dest_id = False
        if self.type_id:
            self.location_dest_id = self.type_id.default_finished_prod_location_id.id

    @api.depends("type_id")
    def _compute_allowed_location(self):
        for mo in self:
            self.allowed_location_src_ids = []
            self.allowed_location_dest_ids = []
            if mo.type_id:
                mo.allowed_location_src_ids = (
                    mo.type_id.allowed_raw_material_location_ids.ids
                )
                mo.allowed_location_dest_ids = (
                    mo.type_id.allowed_finished_prod_location_ids.ids
                )

    allowed_location_src_ids = fields.Many2many(
        string="Allowed Raw Materials Location",
        comodel_name="stock.location",
        compute="_compute_allowed_location",
        store=False,
    )
    allowed_location_dest_ids = fields.Many2many(
        string="Allowed Finished Products Location",
        comodel_name="stock.location",
        compute="_compute_allowed_location",
        store=False,
    )
