# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    remarks = fields.Char(compute='get_remark_terms_and_conditions')
    installation_date = fields.Date(compute="get_installation_date")

    def get_installation_date(self):
        for rec in self:
            if rec.sale_id:
                rec.installation_date = " ".join([str(n.start_date) for n in rec.sale_id.order_line if n.start_date != False])


    def get_remark_terms_and_conditions(self):
        for rec in self:
            if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms'):
                rec.remarks = self.env.company.invoice_terms
