# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MrpProductionType(models.Model):
    _inherit = "mrp.production_type"

    default_raw_material_location_id = fields.Many2one(
        string="Default Raw Material Location",
        domain="[('usage', '=', 'internal')]",
        comodel_name="stock.location",
    )

    allowed_raw_material_location_ids = fields.Many2many(
        string="Allowed Raw Materials Location",
        comodel_name="stock.location",
        domain="[('usage', '=', 'internal')]",
        relation="mo_type_raw_location_rel",
        column1="mo_type_id",
        column2="location_id",
    )

    default_finished_prod_location_id = fields.Many2one(
        string="Default Finished Product Location",
        domain="[('usage', '=', 'internal')]",
        comodel_name="stock.location",
    )

    allowed_finished_prod_location_ids = fields.Many2many(
        string="Allowed Finished Products Location",
        comodel_name="stock.location",
        domain="[('usage', '=', 'internal')]",
        relation="mo_type_finished_location_rel",
        column1="mo_type_id",
        column2="location_id",
    )
