# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, tools


class MrpProductionMassInReport(models.Model):
    _name = "mrp.production_mass_in_report"
    _description = "Production Order Mass In Report"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    move_id = fields.Many2one(string="Stock Move", comodel_name="stock.move")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    date = fields.Datetime(
        string="Date",
    )
    quantity = fields.Float(string="Quantity")

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            a.id AS move_id,
            b.id AS production_id,
            a.product_id AS product_id,
            a.date AS date,
            CASE
                WHEN f.coefficient IS NOT NULL
                    THEN a.product_qty * f.coefficient
                ELSE
                    0.0
            END AS quantity
        """
        return select_str

    def _from(self):
        from_str = """
        stock_move AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
            AND a.state = 'done'
            AND b.state = 'done'
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN mrp_production AS b ON
            a.raw_material_production_id = b.id
        JOIN product_product AS c ON
            a.product_id = c.id
        JOIN product_template AS d ON
            c.product_tmpl_id = d.id
        JOIN res_company AS e ON
            a.company_id = e.id
        LEFT JOIN product_uom_conversion AS f ON
            d.id = f.product_template_id
            AND e.mass_balance_uom_id = f.reference_uom_id
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
