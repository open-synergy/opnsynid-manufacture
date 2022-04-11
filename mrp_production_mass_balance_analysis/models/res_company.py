# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    mass_balance_uom_id = fields.Many2one(
        string="Mass Balance UoM",
        comodel_name="product.uom",
    )
