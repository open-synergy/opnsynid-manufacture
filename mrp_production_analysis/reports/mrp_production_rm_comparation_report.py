# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, tools


class MrpProductionRmComparation(models.Model):
    _name = "mrp.production_rm_comparation_report"
    _description = "Production Order RM Comparation Report"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    date_planned = fields.Datetime(
        string="Schedulled Date",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    categ_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
    )
    bom_id = fields.Many2one(
        string="BoM",
        comodel_name="mrp.bom",
    )
    location_src_id = fields.Many2one(
        string="Raw Material Location",
        comodel_name="stock.location",
    )
    location_dest_id = fields.Many2one(
        string="Finished Product Location",
        comodel_name="stock.location",
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
        SELECT
            chr(a.production_id) || chr(a.product_id) AS id,
            a.production_id AS production_id,
            b.date_planned AS date_planned,
            a.product_id AS product_id,
            d.categ_id AS categ_id,
            b.user_id AS user_id,
            b.bom_id AS bom_id,
            b.location_src_id AS location_src_id,
            b.location_dest_id AS location_dest_id,
            SUM(a.plan_quantity) AS plan_quantity,
            SUM(a.realization_quantity) AS realization_quantity,
            SUM(a.difference) AS difference
        """
        return select_str

    def _from(self):
        from_str = """
        mrp_production_rm_analysis AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1 AND
            b.state = 'done'
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN mrp_production AS b ON
            a.production_id = b.id
        JOIN product_product AS c ON
            a.product_id = c.id
        JOIN product_template AS d ON
            c.product_tmpl_id = d.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY
            a.production_id,
            a.product_id,
            b.date_planned,
            a.product_id,
            d.categ_id,
            b.user_id,
            b.bom_id,
            b.location_src_id,
            b.location_dest_id
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
