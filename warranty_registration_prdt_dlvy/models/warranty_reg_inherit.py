from odoo import models, fields, api


class WarrantySettings(models.TransientModel):
    _inherit = 'warranty.settings'

    create_once_delivered = fields.Boolean(string="Create Warranty Once Delivered")
    create_warranty_from_saleorder = fields.Boolean('Create Warranty from Sale Order')

    # @api.onchange('create_once_delivered')
    def warranty_generation_method_selection(self):
        lis_of_objective = ['create_warranty_from_saleorder', 'create_once_delivered']
        for field in lis_of_objective:
            if self.env.context.get('ad_bool_field_name') != field:
                self[field] = False

    @api.model
    def default_get(self, flds):
        result = super(WarrantySettings, self).default_get(flds)
        create_once_delivered = self.env['ir.config_parameter'].sudo().get_param('warranty_registration_prdt_dlvy.create_once_delivered')
        create_warranty_from_saleorder = self.env['ir.config_parameter'].sudo().get_param(
            'warranty_registration_prdt_dlvy.create_warranty_from_saleorder')
        
        
        result['create_once_delivered'] = create_once_delivered
        result['create_warranty_from_saleorder'] = create_warranty_from_saleorder
        return result

    def set_values(self):
        super(WarrantySettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('warranty_registration_prdt_dlvy.create_once_delivered',
                                                         self.create_once_delivered)
        self.env['ir.config_parameter'].sudo().set_param('warranty_registration_prdt_dlvy.create_warranty_from_saleorder',
                                                         self.create_warranty_from_saleorder)
        # module = False
        # if self.create_warranty_from_saleorder == True:
        #     module = self.env['ir.module.module'].search(
        #         [('state', '!=', 'installed'), ('name', '=', 'v9_sale_invoice_serial')])
        # if module:
        #     module.button_immediate_install()

        

