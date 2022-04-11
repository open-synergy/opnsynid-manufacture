# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, tools


class MrpProductionAllRm(models.Model):
    _name = "mrp.production_all_rm"
    _description = "Production Order All RM"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )

    def _select(self):
        select_str = """
        SELECT DISTINCT
            row_number() OVER() as id,
            a.production_id as production_id,
            a.product_id as product_id
        """
        return select_str

    def _from(self):
        from_str = """
        (
        SELECT  a1.production_id,
                a1.product_id
        FROM    mrp_production_rm_plan_summary AS a1
        UNION
        SELECT  a2.production_id,
                a2.product_id
        FROM    mrp_production_rm_realization_summary AS a2
        ) AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
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
