# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class sale_order_scan_wizard(models.TransientModel):
    _name = "sale.order.scan"
    _description = 'Sale Order Scan Wizard'

    scan = fields.Char(string="Scan")


    def add_product_via_scan_wizard(self):
        if self.scan:
            Product = self.env['stock.production.lot']
            order = self.env['sale.order'].browse(self._context.get('active_id'))
            products_ids = Product.search([('name', '=', self.scan)])
            if not products_ids:
                raise Warning(_(' %s Serial number is not available in system!!') % self.scan)
 
            line_list = []
            serial_no_list = []
            if order.pricelist_id.discount_policy == 'with_discount':

                for product in products_ids:
                    if product.product_id.uom_id:
                        price =dict((product_id, res_tuple[0]) for product_id, res_tuple in order.pricelist_id._compute_price_rule([(product.product_id, product.product_qty, order.partner_id)], date=False, uom_id=product.product_id.uom_id.id).items())
                        pricelst_price = price.get(product.product_id.id, 0.0)

                    if not product.product_qty > 0.0 :
                        raise Warning(_('Stock not available with %s serial/lot number.') % self.scan)
                    for line in order.order_line :
                        serial_no_list.append(line.serial_no.id)
                    if product.id in serial_no_list :
                        self.scan = ''
                        raise Warning(_('This Serial Number/Lot Is Already In Sale Order Line!!'))
                    else :

                        if product.product_qty > 0.0 :
                            vals = {
                                'order_id': order.id,
                                'product_id': product.product_id.id,
                                'name': product.product_id.name,
                                'product_uom_qty': product.product_qty,
                                'price_unit': pricelst_price,
                                'product_uom': product.product_id.product_tmpl_id.uom_id.id,
                                'state': 'draft',
                                'serial_no':product.id or False,
                                'tax_id': [(6, 0, product.product_id.taxes_id.ids)],
                            }
                            line_list.append((0, 0 , vals))
                order.write({'order_line' : line_list})
                self.scan = ''
                return
            else:
                for product in products_ids:
                    if product.product_id.uom_id:
                        price =dict((product_id, res_tuple[0]) for product_id, res_tuple in order.pricelist_id._compute_price_rule([(product.product_id, product.product_qty, order.partner_id)], date=False, uom_id=product.product_id.uom_id.id).items())
                        pricelst_price = price.get(product.product_id.id, 0.0)                    
                        fix_discount = []
                    product_temp_obj = self.env['product.template'].search([('name','=',product.product_id.name)],limit=1)
                    
                    for pricelist in order.pricelist_id.item_ids:
                        if pricelist.min_quantity <= product.product_qty:
                            if pricelist.date_end:
                                if pricelist.date_end <= date.today():
                                    fix_discount.append(0.0)
                            if pricelist.applied_on == '3_global':
                                if pricelist.compute_price == 'fixed':
                                    if pricelist.fixed_price < product.product_id.lst_price:
                                        fixed_value = ((pricelist.fixed_price - product.product_id.lst_price)/product.product_id.lst_price)*100
                                        fix_discount.append(abs(fixed_value))
                                elif pricelist.compute_price == 'percentage':
                                    fix_discount.append(pricelist.percent_price)
                            elif pricelist.applied_on == '2_product_category' and pricelist.categ_id.id == self.product_id.categ_id.id or pricelist.categ_id.id == product.product_id.categ_id.id:
                                if pricelist.compute_price == 'fixed':
                                    if pricelist.fixed_price < product.product_id.lst_price:
                                        fixed_value = ((pricelist.fixed_price - product.product_id.lst_price)/product.product_id.lst_price)*100
                                        fix_discount.append(abs(fixed_value))
                                elif pricelist.compute_price == 'percentage':
                                    fix_discount.append(pricelist.percent_price)
                            elif pricelist.applied_on == '1_product' and pricelist.product_tmpl_id.id == product_temp_obj.id:
                                if pricelist.compute_price == 'fixed':
                                    if pricelist.fixed_price < product.product_id.lst_price:
                                        fixed_value = ((pricelist.fixed_price - product.product_id.lst_price)/product.product_id.lst_price)*100
                                        fix_discount.append(abs(fixed_value))
                                elif pricelist.compute_price == 'percentage':
                                    fix_discount.append(pricelist.percent_price)
                            elif pricelist.applied_on == '0_product_variant' and pricelist.product_id.id == product.product_id.id:
                                if pricelist.compute_price == 'fixed':
                                    if pricelist.fixed_price < product.product_id.lst_price:
                                        fixed_value = ((pricelist.fixed_price - product.product_id.lst_price)/product.product_id.lst_price)*100
                                        fix_discount.append(abs(fixed_value))
                                elif pricelist.compute_price == 'percentage':
                                    fix_discount.append(pricelist.percent_price)
                    if fix_discount:
                        discount = fix_discount[0]
                    else:
                        discount = 0.0
                    if pricelist.fixed_price > product.product_id.lst_price or pricelist.compute_price == 'formula':
                        price = pricelst_price
                    else:
                        price = product.product_id.lst_price
                    
                    if not product.product_qty > 0.0 :
                        raise Warning(_('Stock not available with %s serial/lot number.') % self.scan)
                    for line in order.order_line :
                        serial_no_list.append(line.serial_no.id)
                    if product.id in serial_no_list :
                        self.scan = ''
                        raise Warning(_('This Serial Number/Lot Is Already In Sale Order Line!!'))
                    else :

                        if product.product_qty > 0.0 :
                            vals = {
                                'order_id': order.id,
                                'product_id': product.product_id.id,
                                'name': product.product_id.name,
                                'product_uom_qty': product.product_qty,
                                'price_unit': price,
                                'product_uom': product.product_id.product_tmpl_id.uom_id.id,
                                'state': 'draft',
                                'serial_no':product.id or False,
                                'tax_id': [(6, 0, product.product_id.taxes_id.ids)],
                            }
                            line_list.append((0, 0 , vals))
                order.write({'order_line' : line_list})
                self.scan = ''
                return

