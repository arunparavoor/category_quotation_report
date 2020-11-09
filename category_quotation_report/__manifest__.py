{
    'name': 'Category Wise Vendor Quotation Report',
    'version': '1.0',
    'category': 'Purchase',    
    'author': 'Arun Reghu Kumar',
    'website':'http://tech4logic.wordpress.com/',
    'depends': ['base','purchase','purchase_requisition','sale_stock'],
    'summary': 'Product Category wise Puchase Quotation Report',
    'description': "Product Category Wise Vendor Quotation Report",
    'data': [
        "security/ir.model.access.csv",
        "wizard/category_quotation_report.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
