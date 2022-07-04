from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta


class StockImmediateTransferInherit(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        res = super(StockImmediateTransferInherit, self).process()
        sale_order = self.env['sale.order'].search([('id', "=", self.env.context.get('active_id'))])

        create_once_delivered = bool(self.env['ir.config_parameter'].sudo().get_param(
            "warranty_registration_prdt_dlvy.create_once_delivered"))
        create_warranty_with_saleorder = bool(self.env['ir.config_parameter'].sudo().get_param(
            "warranty_registration_prdt_dlvy.create_warranty_with_saleorder"))
        for line in sale_order.order_line :
            if 'serial_no' in sale_order.env['sale.order.line']._fields:
                if line.serial_no and create_once_delivered == True and create_warranty_with_saleorder == False and line.product_id.under_warranty == True:
                    self.env['product.warranty'].create({
                        'partner_id' : sale_order.partner_id.id,
                        'product_id' : line.product_id.id,
                        'phone' : sale_order.partner_id.phone,
                        'email' : sale_order.partner_id.email,
                        'product_serial_id' : line.serial_no.id,
                        'so_id' : sale_order.id,
                        'warranty_create_date': fields.date.today(),
                        'warranty_end_date': fields.date.today() + relativedelta(months=line.product_id.warranty_period)
                                            # if line.product_id.warranty_period != 0 else " ",
                    })
            line.update({'start_date': fields.date.today(),
                         'end_date': fields.date.today() + relativedelta(months=line.product_id.warranty_period)})
        return res



