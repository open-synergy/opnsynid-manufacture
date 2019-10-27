# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class MrpProductionMassBalanceAnalysis(models.Model):
    _name = "mrp.production_mass_balance_analysis"
    _description = "Production Order Mass Balance Analysis"
    _auto = False

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
    )
    date_planned = fields.Datetime(
        string="Schedulled Date",
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
    mass_in_quantity = fields.Float(
        string="Mass In Quantity"
    )
    mass_out_quantity = fields.Float(
        string="Mass Out Quantity"
    )
    loss_quantity = fields.Float(
        string="Loss Quantity"
    )
    in_out_comparison = fields.Float(
        string="In/Out Comparison"
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            b.production_id AS production_id,
            a.date_planned AS date_planned,
            a.user_id AS user_id,
            a.bom_id AS bom_id,
            a.location_src_id AS location_src_id,
            a.location_dest_id AS location_dest_id,
            SUM(b.mass_in_quantity) AS mass_in_quantity,
            SUM(b.mass_out_quantity) AS mass_out_quantity,
            SUM(b.loss_quantity) AS loss_quantity,
            CASE
                WHEN
                    SUM(b.mass_out_quantity) > 0.0
                    THEN
                    SUM(b.mass_in_quantity) / SUM(b.mass_out_quantity)
                ELSE
                    0.0
                END AS in_out_comparison
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
        JOIN mrp_production_mass_balance_report AS b ON
            a.id = b.production_id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY
            a.id,
            b.production_id,
            a.date_planned,
            a.user_id,
            a.bom_id,
            a.location_src_id,
            a.location_dest_id
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
