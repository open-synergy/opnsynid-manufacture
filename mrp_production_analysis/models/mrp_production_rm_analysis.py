# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, tools


class MrpProductionRmAnalysis(models.Model):
    _name = "mrp.production_rm_analysis"
    _description = "Production Order RM Analysis"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    plan_quantity = fields.Float(
        string="Plan Quantity",
    )
    realization_quantity = fields.Float(
        string="Realization Quantity",
    )
    difference = fields.Float(
        string="Diff",
    )

    def _select(self):
        select_str = """
        SELECT DISTINCT
            row_number() OVER() as id,
            a.production_id as production_id,
            a.product_id as product_id,
            CASE
                WHEN b.quantity IS NOT NULL
                    THEN b.quantity
                ELSE 0.0
            END AS plan_quantity,
            CASE
                WHEN c.quantity IS NOT NULL
                    THEN c.quantity
                ELSE 0.0
            END AS realization_quantity,
            ((CASE
                WHEN c.quantity IS NOT NULL
                    THEN c.quantity
                ELSE 0.0
            END) -
            (CASE
                WHEN b.quantity IS NOT NULL
                    THEN b.quantity
                ELSE 0.0
            END)) AS difference
        """
        return select_str

    def _from(self):
        from_str = """
        mrp_production_all_rm AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        LEFT JOIN mrp_production_rm_plan_summary AS b ON
            a.production_id = b.production_id AND
            a.product_id = b.product_id
        LEFT JOIN mrp_production_rm_realization_summary AS c ON
            a.production_id = c.production_id AND
            a.product_id = c.product_id
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
