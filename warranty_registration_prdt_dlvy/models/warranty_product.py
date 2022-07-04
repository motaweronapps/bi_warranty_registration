from odoo import models, fields, api


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	create_once_delivered = fields.Boolean('create Warranty Once Delivered')
	warranty_delivery_config = fields.Boolean(compute="get_warranty_delivery_config")

	def get_warranty_delivery_config(self):
		tmp = self.env['warranty.settings'].search([], order="id desc", limit=1).create_once_delivered
		for line in self:
			line.warranty_delivery_config = tmp

	def write(self, vals):
		res = super(ProductTemplate, self).write(vals)
		product_product = self.env['product.product'].search([('product_tmpl_id','=',self.id)])

		if 'create_once_delivered' in vals :
			for line in product_product :
				line.create_once_delivered = vals['create_once_delivered']
		return res


class product_product(models.Model):
	_inherit = 'product.product'

	create_once_delivered = fields.Boolean('create Warranty Once Delivered')
	warranty_delivery_config = fields.Boolean(compute="get_warranty_delivery_config")

	def get_warranty_delivery_config(self):
		tmp = self.env['warranty.settings'].search([], order="id desc", limit=1).create_once_delivered
		for line in self:
			line.warranty_delivery_config = tmp

	@api.model
	def create(self, vals):
		res = super(product_product, self).create(vals)
		template = res.product_tmpl_id
		if template:
			if template.create_once_delivered:
				res.create_once_delivered = template.create_once_delivered
			else:
				template.create_once_delivered = res.create_once_delivered

		return res