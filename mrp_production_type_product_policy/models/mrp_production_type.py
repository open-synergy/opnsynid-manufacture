# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpProductionType(models.Model):
    _inherit = "mrp.production_type"

    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_mrp_prod_type_2_product",
        column1="type_id",
        column2="product_id",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_mrp_prod_type_2_product_categ",
        column1="type_id",
        column2="categ_id",
    )
    restrict_product = fields.Boolean(
        string="Restrict Product",
    )
