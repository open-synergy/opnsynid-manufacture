# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class QcTest(models.Model):
    _inherit = "qc.test"

    auto_lock_lot = fields.Boolean(
        string="Lock Lot When Inspection Start",
    )
    auto_unlock_lot = fields.Boolean(
        string="Unlock Lot When Inspection Succeded",
    )
