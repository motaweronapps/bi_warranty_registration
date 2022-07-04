# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class sale_order_line(models.Model):
	_inherit = "sale.order.line"

	serial_no =  fields.Many2one('stock.production.lot',string='Serial Number',domain="[('product_id', '=', product_id)]")

	def _prepare_invoice_line(self, **optional_values):
		res = super(sale_order_line, self)._prepare_invoice_line(**optional_values)
		res.update({'serial_no':self.serial_no.id})
		return res
