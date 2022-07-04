# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import UserError


class stock_move(models.Model):
	_inherit = "stock.move"

	serial_no =  fields.Many2one('stock.production.lot',string='Serial Number',domain="[('product_id', '=', product_id)]")   

	def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
		self.ensure_one()
		# apply putaway
		location_dest_id = self.location_dest_id._get_putaway_strategy(self.product_id).id or self.location_dest_id.id
		vals = {
			'move_id': self.id,
			'product_id': self.product_id.id,
			'product_uom_id': self.product_uom.id,
			'location_id': self.location_id.id,
			'location_dest_id': location_dest_id,
			'picking_id': self.picking_id.id,
		}
		if quantity:
			uom_quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom, rounding_method='HALF-UP')
			uom_quantity_back_to_product_uom = self.product_uom._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
			rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
			if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
				vals = dict(vals, product_uom_qty=uom_quantity)
			else:
				vals = dict(vals, product_uom_qty=quantity, product_uom_id=self.product_id.uom_id.id)
		if reserved_quant:
			if self.serial_no:
				vals = dict(
					vals,
					location_id=reserved_quant.location_id.id,
					lot_id=self.serial_no.id or False,
					package_id=reserved_quant.package_id.id or False,
					owner_id =reserved_quant.owner_id.id or False,
				)
			else:
				vals = dict(
					vals,
					location_id=reserved_quant.location_id.id,
					lot_id=reserved_quant.lot_id.id or False,
					package_id=reserved_quant.package_id.id or False,
					owner_id =reserved_quant.owner_id.id or False,
				)				
		return vals

	def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None, owner_id=None, strict=True):
		""" Create or update move lines.
		"""
		self.ensure_one()

		if not lot_id:
			if self.serial_no:
				lot_id = self.serial_no
			else:
				lot_id = self.env['stock.production.lot']
		if not package_id:
			package_id = self.env['stock.quant.package']
		if not owner_id:
			owner_id = self.env['res.partner']

		taken_quantity = min(available_quantity, need)

		if not strict:
			taken_quantity_move_uom = self.product_id.uom_id._compute_quantity(taken_quantity, self.product_uom, rounding_method='DOWN')
			taken_quantity = self.product_uom._compute_quantity(taken_quantity_move_uom, self.product_id.uom_id, rounding_method='HALF-UP')

		quants = []

		if self.product_id.tracking == 'serial':
			rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
			if float_compare(taken_quantity, int(taken_quantity), precision_digits=rounding) != 0:
				taken_quantity = 0

		try:
			with self.env.cr.savepoint():
				if not float_is_zero(taken_quantity, precision_rounding=self.product_id.uom_id.rounding):
					quants = self.env['stock.quant']._update_reserved_quantity(
						self.product_id, location_id, taken_quantity, lot_id=lot_id,
						package_id=package_id, owner_id=owner_id, strict=strict
					)
		except UserError:
			taken_quantity = 0

		# Find a candidate move line to update or create a new one.
		for reserved_quant, quantity in quants:
			to_update = self.move_line_ids.filtered(lambda ml: ml._reservation_is_updatable(quantity, reserved_quant))
			if to_update:
				to_update[0].with_context(bypass_reservation_update=True).product_uom_qty += self.product_id.uom_id._compute_quantity(quantity, to_update[0].product_uom_id, rounding_method='HALF-UP')
			else:
				if self.product_id.tracking == 'serial':
					for i in range(0, int(quantity)):
						self.env['stock.move.line'].create(self._prepare_move_line_vals(quantity=1, reserved_quant=reserved_quant))
				else:
					self.env['stock.move.line'].create(self._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant))
		return taken_quantity

