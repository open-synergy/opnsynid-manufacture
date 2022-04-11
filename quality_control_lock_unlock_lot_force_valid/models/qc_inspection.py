# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    @api.multi
    def action_confirm(self):
        _super = super(QcInspection, self)
        _super.action_confirm()
        for inspection in self:
            if inspection._check_auto_unlock_lot():
                inspection.lot.write(inspection._prepare_unlock_lot_data())

    @api.multi
    def action_approve(self):
        _super = super(QcInspection, self)
        _super.action_approve()
        for inspection in self:
            if inspection._check_auto_unlock_lot():
                inspection.lot.write(inspection._prepare_unlock_lot_data())
