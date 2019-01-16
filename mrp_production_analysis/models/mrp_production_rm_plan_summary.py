# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class MrpProductionRmPlanSummary(models.Model):
    _name = "mrp.production_rm_plan_summary"
    _description = "Production Order RM Realization Summary"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    quantity = fields.Float(
        string="Quantity",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            b.id AS production_id,
            a.product_id AS product_id,
            SUM(a.product_qty) AS quantity
        """
        return select_str

    def _from(self):
        from_str = """
                mrp_production_product_line AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
            AND a.addition IS NOT TRUE
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN mrp_production AS b ON
            a.production_id = b.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY
            b.id,
            a.product_id
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
