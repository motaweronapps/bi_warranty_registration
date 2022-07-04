{
    'name': 'Warranty Registration On product delivery',
    'category': 'Industries',
    'summary' : "Warranty will create once the product delivers",
    'author': "sgib",
    'depends': ['bi_warranty_registration','base','sale_management','account','product','stock','mail', 'crm'],
    'version': '14.0.0.0',

    'data': ['views/warranty_reg_inherit.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}