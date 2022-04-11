# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class GroupStockMoveConsume(models.TransientModel):
    _name = "stock.group_move_consume"
    _description = "Group Consume Product"

    @api.model
    def _default_production_id(self):
        return self.env.context.get("active_id", False)

    @api.model
    def _default_line_ids(self):
        mo_id = self.env.context.get("active_id", False)
        mo = self.env["mrp.production"].browse([mo_id])[0]
        result = []
        for move in mo.move_lines:
            result.append(
                (
                    0,
                    0,
                    {
                        "move_id": move.id,
                        "product_id": move.product_id.id,
                        "product_qty": move.product_uom_qty,
                        "product_uom": move.product_uom.id,
                        "location_id": move.location_id.id,
                    },
                )
            )
        return result

    production_id = fields.Many2one(
        string="# MO",
        comodel_name="mrp.production",
        default=lambda self: self._default_production_id(),
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="stock.move.consume",
        inverse_name="wizard_id",
        default=lambda self: self._default_line_ids(),
    )

    @api.multi
    def action_consume(self):
        self.ensure_one()
        self._action_consume()

    @api.multi
    def _action_consume(self):
        for move in self.line_ids:
            ctx = {
                "active_model": "stock.move",
                "active_ids": [move.move_id.id],
            }
            move.with_context(ctx).do_move_consume()


class StockMoveConsume(models.TransientModel):
    _inherit = "stock.move.consume"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="stock.group_move_consume",
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="stock.move",
    )
