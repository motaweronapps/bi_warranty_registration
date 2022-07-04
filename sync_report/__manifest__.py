# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Delivery Report",
    'summary': """ Report """,
    'description': """  """,
    'author': "Synconics Technologies Pvt. Ltd.",
    'website': "http://www.synconics.com",
    'category': 'stock',
    'version': '1.0',
    'sequence': 20,
    'license': 'OPL-1',
    'depends': ['stock', 'sale'],
    'data': [
        'report/report_action.xml',
        'report/delivery_slip_report.xml',
        'report/product_trial_report.xml',
        'report/sale_order.xml',
        'views/assets_trial_report_external.xml',
        'views/sale_order.xml',
    ],
    'demo': [
        ''
        ],
    'qweb': [
    ],

    'images': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
