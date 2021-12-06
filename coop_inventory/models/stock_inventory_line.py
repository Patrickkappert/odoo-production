# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'
    line_ids = fields.One2many(
        copy=False)

class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.one
    @api.depends('location_id', 'product_id', 'package_id', 'product_uom_id',
        'company_id', 'prod_lot_id', 'partner_id', 'inventory_id.date')
    def _compute_theoretical_qty(self):
        if not self.product_id:
            self.theoretical_qty = 0
            return
        product_at_date = self.env['product.product'].with_context({
            'to_date': self.inventory_id.date,
            'location': self.location_id.id,
            'compute_child': False,
            'lot_id': self.prod_lot_id.id,
            'package_id': self.package_id.id,
        }).browse(self.product_id.id)
        theoretical_qty = product_at_date.qty_available
        if theoretical_qty and self.product_uom_id and \
                self.product_id.uom_id != self.product_uom_id:
            theoretical_qty = self.product_id.uom_id._compute_quantity(
                theoretical_qty, self.product_uom_id)
        self.theoretical_qty = theoretical_qty
