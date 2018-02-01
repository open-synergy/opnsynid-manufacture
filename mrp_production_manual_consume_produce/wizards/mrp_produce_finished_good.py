# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class GrpupProduceFinishedGood(models.TransientModel):
    _name = "mrp.group_produce_finished_good"
    _description = "Group Produce Finished Good"

    @api.model
    def _default_line_ids(self):
        mo_id = self.env.context.get("active_id", False)
        mo = self.env["mrp.production"].browse([mo_id])[0]
        result = []
        for move in mo.move_created_ids:
            result.append((0, 0, {
                "move_id": move.id,
                "product_id": move.product_id.id,
                "product_qty": move.product_uom_qty,
                "uom_id": move.product_uom.id,
            }))
        return result

    line_ids = fields.One2many(
        string="Produce Goods",
        comodel_name="mrp.produce_finished_good",
        inverse_name="wizard_id",
        default=lambda self: self._default_line_ids(),
    )

    @api.multi
    def action_produce(self):
        for wiz in self:
            wiz._produce()

    @api.model
    def _produce(self):
        self.ensure_one()
        for line in self.line_ids:
            line.button_produce()


class ProduceFinishedGood(models.TransientModel):
    _name = "mrp.produce_finished_good"
    _description = "Produce Finished Good"

    @api.model
    def _default_product_id(self):
        active_model = self.env.context.get("active_model", False)
        if active_model != "stock.move":
            return False
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_id.id

    @api.model
    def _default_uom_id(self):
        active_model = self.env.context.get("active_model", False)
        if active_model != "stock.move":
            return False
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_uom.id

    @api.model
    def _default_product_qty(self):
        active_model = self.env.context.get("active_model", False)
        if active_model != "stock.move":
            return False
        move_id = self.env.context.get("active_id", False)
        move = self.env["stock.move"].browse([move_id])[0]
        return move.product_uom_qty

    @api.model
    def _default_move_id(self):
        active_model = self.env.context.get("active_model", False)
        if active_model != "stock.move":
            return False
        move_id = self.env.context.get("active_id", False)
        return move_id

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="mrp.group_produce_finished_good",
    )
    move_id = fields.Many2one(
        string="Move",
        comodel_name="stock.move",
        required=True,
        default=lambda self: self._default_move_id(),
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        readonly=True,
        default=lambda self: self._default_product_id(),
    )
    product_qty = fields.Float(
        string="Qty. Produced",
        default=lambda self: self._default_product_qty(),
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        default=lambda self: self._default_uom_id(),
        readonly=True,
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
    )

    @api.multi
    def button_produce(self):
        self.ensure_one()
        lot_id = self._get_lot_id()
        new_move_ids = self.move_id.action_consume(
            self.product_qty,
            restrict_lot_id=lot_id)
        self.env["stock.move"].browse(new_move_ids).write({
            "production_id": self.move_id.production_id.id,
        })
        return True

    @api.multi
    def _get_lot_id(self):
        self.ensure_one()
        return self.lot_id and self.lot_id.id or False
