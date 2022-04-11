# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import SUPERUSER_ID, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_policy(self):
        for mo in self:
            if self.env.user.id == SUPERUSER_ID:
                mo.confirm_ok = (
                    mo.produce_ok
                ) = mo.check_ok = mo.force_ok = mo.start_ok = mo.cancel_ok = True
                continue

            if mo.type_id:
                mo_type = mo.type_id
                for policy in mo_type._get_mo_button_policy_map():
                    setattr(
                        mo,
                        policy[0],
                        mo_type._get_mo_button_policy(policy[1]),
                    )

    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    produce_ok = fields.Boolean(
        string="Can Produce",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    check_ok = fields.Boolean(
        string="Can Check Availability",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    force_ok = fields.Boolean(
        string="Can Force Reservation",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
