from odoo import models, fields, api


class StockProductsLotsInherit(models.Model):
    _inherit = 'stock.production.lot'

    color = fields.Char('Color', compute='compute_custom_fields')
    pi_number = fields.Char('Vendor Reference')
    cost = fields.Float(related='product_id.standard_price')
    ware_house = fields.Char('Ware House')

    def compute_custom_fields(self):
        stock_move_line = self.env['stock.move.line']
        for rec in self:
            current_id = stock_move_line.search([('lot_id', '=', rec.id)])
            color = 'No color selected' if ' '.join([n.name for n in rec.product_id.product_template_attribute_value_ids if 'Color' in n.display_name]) == "" else ' '.join([n.name for n in rec.product_id.product_template_attribute_value_ids if 'Color' in n.display_name])
            ware_house = ' '.join([n.display_name for n in current_id.location_dest_id])
            pi_number = '' if not ' '.join([str(n.partner_ref) for n in rec.purchase_order_ids if n]) else ' '.join([str(n.partner_ref) for n in rec.purchase_order_ids if n])
            vals = {'color':color, 'ware_house':ware_house, 'pi_number':pi_number}
            rec.write(vals)

