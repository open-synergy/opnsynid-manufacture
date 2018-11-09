# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class MrpProductionType(models.Model):
    _inherit = "mrp.production_type"

    mo_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm MO",
        comodel_name="res.groups",
        relation="rel_mo_allowed_confirm_groups",
        column1="type_id",
        column2="group_id",
    )
    mo_produce_grp_ids = fields.Many2many(
        string="Allowed To Produce MO",
        comodel_name="res.groups",
        relation="rel_mo_allowed_produce_groups",
        column1="type_id",
        column2="group_id",
    )
    mo_check_grp_ids = fields.Many2many(
        string="Allowed To Check MO Availability",
        comodel_name="res.groups",
        relation="rel_mo_allowed_check_groups",
        column1="type_id",
        column2="group_id",
    )
    mo_force_grp_ids = fields.Many2many(
        string="Allowed To Force Reservation MO",
        comodel_name="res.groups",
        relation="rel_mo_allowed_force_groups",
        column1="type_id",
        column2="group_id",
    )
    mo_start_grp_ids = fields.Many2many(
        string="Allowed To Start MO",
        comodel_name="res.groups",
        relation="rel_mo_allowed_start_groups",
        column1="type_id",
        column2="group_id",
    )
    mo_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel MO",
        comodel_name="res.groups",
        relation="rel_mo_allowed_cancel_groups",
        column1="type_id",
        column2="group_id",
    )

    @api.model
    def _get_mo_button_policy_map(self):
        return [
            ("confirm_ok", "mo_confirm_grp_ids"),
            ("produce_ok", "mo_produce_grp_ids"),
            ("check_ok", "mo_check_grp_ids"),
            ("force_ok", "mo_force_grp_ids"),
            ("start_ok", "mo_start_grp_ids"),
            ("cancel_ok", "mo_cancel_grp_ids"),
        ]

    @api.multi
    def _get_mo_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids += getattr(
            self, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result
