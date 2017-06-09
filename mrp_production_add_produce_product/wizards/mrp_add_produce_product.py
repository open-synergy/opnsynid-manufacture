# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class AddProduceProduct(models.TransientModel):
    _name = "mrp.add_produce_product"
    _description = "Add Produce Products"

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    product_qty = fields.Float(
        string="Qty. Produced",
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )

    @api.onchange("product_id")
    def onchange_uom(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    @api.multi
    def button_add(self):
        self.ensure_one()
        obj_move = self.env["stock.move"]
        move = obj_move.create(
            self._prepare_additional_produce_product())
        move.action_confirm()
        return True

    @api.multi
    def _prepare_additional_produce_product(self):
        self.ensure_one()
        production_id = self.env.context.get("active_id", False)
        production = self.env["mrp.production"].browse([production_id])[0]
        src_loc = self.product_id.property_stock_production
        data = {
            "name": self.product_id.name,
            "date": production.date_planned,
            "product_id": self.product_id.id,
            "product_uom": self.uom_id.id,
            "product_uom_qty": self.product_qty,
            "product_uos_qty": (production.product_uos and
                                production.product_uos_qty or False),
            "product_uos": (production.product_uos and
                            production.product_uos.id or False),
            "location_id": src_loc.id,
            "location_dest_id": production.location_dest_id.id,
            "company_id": production.company_id.id,
            "production_id": production.id,
            "origin": production.name,
        }
        return data
