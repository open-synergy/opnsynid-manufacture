# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MrpProductionType(models.Model):
    _name = "mrp.production_type"
    _inherit = ["mail.thread"]
    _description = "MO Type"

    name = fields.Char(
        string="MO Type",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
