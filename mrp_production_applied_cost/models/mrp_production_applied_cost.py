# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from datetime import datetime
from openerp import tools


class MrpProductionAppliedCost(models.Model):
    _name = "mrp.production.applied_cost"
    _description = "Manufacturing Order Applied Cost"

    @api.multi
    @api.depends(
        "price_unit",
        "product_qty",
    )
    def _compute_total(self):
        for applied in self:
            applied.amount_total = applied.price_unit * applied.product_qty

    mo_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=datetime.now().strftime("%Y-%m-%d"),
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
    move_id = fields.Many2one(
        string="Journal Entry",
        comodel_name="account.move",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Unposted"),
            ("post", "Posted"),
        ],
        readonly=True,
        required=True,
        default="draft",
    )

    @api.multi
    def button_post(self):
        for applied in self:
            applied.write(self._prepare_post_data())
            self._update_analytic_line()

    @api.multi
    def button_unpost(self):
        for applied in self:
            applied.move_id.unlink()
            applied.write(self._prepare_unpost_data())

    @api.multi
    def _prepare_post_data(self):
        self.ensure_one()
        return {
            "state": "post",
            "move_id": self._create_move().id,
        }

    @api.multi
    def _prepare_unpost_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def _create_move(self):
        self.ensure_one()
        move = self.env["account.move"].create(
            self._prepare_move_data())
        return move

    @api.multi
    def _prepare_move_data(self):
        self.ensure_one()
        return {
            "journal_id": self.journal_id.id,
            "date": self.date,
            "ref": self.mo_id.name,
            "period_id": self._get_period().id,
            "line_id": self._prepare_move_line_data(),
        }

    @api.multi
    def _prepare_move_line_data(self):
        self.ensure_one()
        result = []
        project = self.mo_id.project_id
        result.append((0, 0, {
            "name": self.name,
            "account_id": self.debit_account_id.id,
            "debit": self.amount_total,
            "credit": 0.0,
            "analytic_account_id": project.analytic_account_id.id,
        }))
        result.append((0, 0, {
            "name": self.name,
            "account_id": self.credit_account_id.id,
            "credit": self.amount_total,
            "debit": 0.0,
        }))
        return result

    @api.multi
    def _get_period(self):
        self.ensure_one()
        return self.env["account.period"].find(
            self.date)

    @api.multi
    def _update_analytic_line(self):
        self.ensure_one()
        criteria = [
            ("move_id.move_id", "=", self.move_id.id),
        ]
        lines = self.env["account.analytic.line"].search(criteria)
        lines.write({
            "mrp_production_id": self.mo_id.id,
            "journal_id": self.analytic_journal_id.id,
        })


class MrpProductionAppliedCostSummary(models.Model):
    _name = "mrp.production.applied_cost_summary"
    _description = "Manufacturing Order Applied Cost Summary"
    _auto = False

    mo_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    analytic_journal_id = fields.Many2one(
        string="Applied Cost Category",
        comodel_name="account.analytic.journal",
    )
    amount_total = fields.Float(
        string="Amount Total",
    )

    def _select(self):
        str_select = """
            SELECT  row_number() OVER() AS id,
                    a.mo_id AS mo_id,
                    a.analytic_journal_id AS analytic_journal_id,
                    SUM(a.amount_total) AS amount_total
            """
        return str_select

    def _group_by(self):
        str_group = """
            GROUP BY    a.mo_id,
                        a.analytic_journal_id
            """
        return str_group

    def _from(self):
        str_from = " mrp_production_applied_cost AS a"
        return str_from

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s AS (
            %s
            FROM %s
            %s
            )""" % (
            self._table, self._select(),
            self._from(), self._group_by()))
