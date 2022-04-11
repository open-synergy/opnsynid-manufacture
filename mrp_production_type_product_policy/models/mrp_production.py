# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.depends("type_id")
    def _compute_allowed_product(self):
        for mo in self:
            self.allowed_product_ids = []
            if mo.type_id:
                mo.allowed_product_ids = mo.type_id.allowed_product_ids
                mo.allowed_product_categ_ids = mo.type_id.allowed_product_categ_ids

    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        compute="_compute_allowed_product",
        store=False,
    )

    @api.onchange("type_id")
    def onchange_product(self):
        self.product_id = False
        domain = []
        if self.type_id and self.type_id.restrict_product:
            mo_type = self.type_id
            domain += [
                ("bom_ids", "!=", False),
                "|",
                ("id", "in", mo_type.allowed_product_ids.ids),
                ("categ_id", "in", mo_type.allowed_product_categ_ids.ids),
            ]
        else:
            domain.append(("bom_ids", "!=", False))
        return {"domain": {"product_id": domain}}
