# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class MrpBomAppliedCost(models.Model):
    _name = "mrp.bom.applied_cost"
    _description = "BoM Applied Cost"

    @api.multi
    @api.depends(
        "price_unit",
        "product_qty",
    )
    def _compute_total(self):
        for applied in self:
            applied.amount_total = applied.price_unit * applied.product_qty

    bom_id = fields.Many2one(
        string="BoM",
        comodel_name="mrp.bom",
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    product_qty = fields.Float(
        string="Qty.",
        required=True,
        default=1.0,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )
    amount_total = fields.Float(
        string="Amount Total",
        compute="_compute_total",
        store=True,
    )

    @api.model
    def _default_credit_account_id(self):
        return self.env["ir.property"].get(
            "property_account_expense_categ",
            "product.category").id

    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
        required=True,
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
        required=True,
        default="_default_credit_account_id",
    )
    journal_id = fields.Many2one(
        string="Jurnal",
        comodel_name="account.journal",
        required=True,
    )
    analytic_journal_id = fields.Many2one(
        string="Applied Cost Category",
        comodel_name="account.analytic.journal",
        required=True,
    )

    @api.multi
    def _prepare_production_applied_cost(self, factor):
        self.ensure_one()
        return {
            "name": self.name,
            "product_id": self.product_id.id,
            "product_uom_id": self.product_uom_id.id,
            "product_qty": self.product_qty * factor,
            "price_unit": self.price_unit,
            "debit_account_id": self.debit_account_id.id,
            "credit_account_id": self.credit_account_id.id,
            "journal_id": self.journal_id.id,
            "analytic_journal_id": self.analytic_journal_id.id,
        }
