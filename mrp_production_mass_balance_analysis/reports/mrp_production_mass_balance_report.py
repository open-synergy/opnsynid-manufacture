# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class MrpProductionMassBalanceReport(models.Model):
    _name = "mrp.production_mass_balance_report"
    _description = "Production Order Mass Balance Report"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    mass_in_quantity = fields.Float(
        string="Mass In Quantity"
    )
    mass_out_quantity = fields.Float(
        string="Mass Out Quantity"
    )
    loss_quantity = fields.Float(
        string="Loss Quantity"
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            a.id AS production_id,
            CASE
                WHEN b.quantity IS NOT NULL
                    THEN b.quantity
                ELSE
                    0.0
            END AS mass_in_quantity,
            CASE
                WHEN c.quantity IS NOT NULL
                    THEN c.quantity
                ELSE
                    0.0
            END AS mass_out_quantity,
            (CASE
                WHEN b.quantity IS NOT NULL
                    THEN b.quantity
                ELSE
                    0.0
            END) -
            (CASE
                WHEN c.quantity IS NOT NULL
                    THEN c.quantity
                ELSE
                    0.0
            END) AS loss_quantity
        """
        return select_str

    def _from(self):
        from_str = """
        mrp_production AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
            AND a.state = 'done'
        """
        return where_str

    def _join(self):
        join_str = """
        LEFT JOIN (
            SELECT
                b1.production_id,
                SUM(b1.quantity) AS quantity
            FROM mrp_production_mass_in_report AS b1
            GROUP BY b1.production_id
        ) AS b ON
            a.id = b.production_id
        LEFT JOIN (
            SELECT
                c1.production_id,
                SUM(c1.quantity) AS quantity
            FROM mrp_production_mass_out_report AS c1
            GROUP BY c1.production_id
        ) AS c ON
            a.id = c.production_id
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by()
        ))
