from odoo import models, api


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('product_id')
    def get_correstponding_lotid(self):
        lis = []
        if self.product_id:
            for rec in self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id)]):
                location = [n.location_id for n in rec.quant_ids]
                if self.location_id in location:
                    lis.append(rec.id)
            return {'domain':{'lot_id':[('id','=',lis)]}}