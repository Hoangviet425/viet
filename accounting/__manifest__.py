{
    'name': 'Integrated Accounting System',
    'version': '1.0',
    'summary': 'Comprehensive accounting, sales, purchase, inventory and cash management system',
    'description': """
        A comprehensive module that integrates:
        - Cash Management
        - Accounting
        - Purchase Management
        - Sales Management
        - Invoice Management
        - Warehouse Management
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'category': 'Accounting/Finance',
    'depends': [
        'base',
        'mail',
        'account',
        'stock',
        'purchase',
        'sale_management',
    ],
    'data': [
        # Security
        'security/accounting_security.xml',
        'security/cash_management/ir.model.access.csv',
        'security/accounting/ir.model.access.csv',
        'security/purchase/ir.model.access.csv',
        'security/purchase/purchase_security.xml',
        'security/sale/ir.model.access.csv',
        'security/sale/sale_security.xml',
        'security/invoice/ir.model.access.csv',
        'security/invoice/invoice_security.xml',
        'security/warehouse/ir.model.access.csv',
        'security/warehouse/warehouse_security.xml',
        
        # Views
        'views/main_menu_views.xml',
        'views/cash_management/cash_management_views.xml',
        'views/accounting/accounting_views.xml',
        
        # Purchase views
        'views/purchase/purchase_order_views.xml',
        'views/purchase/vendor_bill_views.xml',
        'views/purchase/purchase_return_views.xml',
        'views/purchase/purchase_dashboard_views.xml',
        'views/purchase/menu_views.xml',
        
        # Sales views
        'views/sale/sale_order_views.xml',
        'views/sale/sale_invoice_views.xml',
        'views/sale/sale_return_views.xml',
        'views/sale/sale_dashboard_views.xml',
        'views/sale/menu_views.xml',
        
        # Invoice views
        'views/invoice/invoice_template_views.xml',
        'views/invoice/invoice_management_views.xml',
        'views/invoice/invoice_processing_views.xml',
        'views/invoice/invoice_dashboard_views.xml',
        'views/invoice/res_config_settings_views.xml',
        'views/invoice/menu_views.xml',
        
        # Warehouse views
        'views/warehouse/warehouse_location_views.xml',
        'views/warehouse/stock_inventory_views.xml',
        'views/warehouse/stock_production_views.xml',
        'views/warehouse/stock_move_views.xml',
        'views/warehouse/stock_operation_views.xml',
        'views/warehouse/stock_picking_views.xml',
        'views/warehouse/warehouse_dashboard_views.xml',
        'views/warehouse/res_config_settings_views.xml',
        'views/warehouse/menu_views.xml',
        
        # Reports
        'report/purchase/purchase_order_report.xml',
        'report/purchase/purchase_return_report.xml',
        'report/purchase/purchase_analysis_report.xml',
        'report/sale/sale_order_report.xml',
        'report/sale/sale_return_report.xml',
        'report/sale/sale_analysis_report.xml',
        'report/invoice/invoice_reports.xml',
        'report/invoice/invoice_templates.xml',
        'report/warehouse/warehouse_reports.xml',
        'report/warehouse/warehouse_templates.xml',
        'report/warehouse/inventory_analysis_report.xml',
        
        # Data
        'security/ir.model.access.csv',
        'views/cash_management_views.xml',
        'views/templates.xml',
        'data/warehouse_data.xml',
        'data/warehouse_sequences.xml',
    ],
     'qweb': [
        'static/src/xml/cash_dashboard.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'accounting/static/src/js/sale_dashboard.js',
            'accounting/static/src/js/invoice_dashboard.js',
            'accounting/static/src/js/warehouse_dashboard.js',
            'accounting/static/src/css/sale_dashboard.css',
            'accounting/static/src/css/invoice_dashboard.css',
            'accounting/static/src/css/warehouse_dashboard.css',
            'accounting/static/src/xml/sale_dashboard.xml',
            'accounting/static/src/xml/invoice_dashboard.xml',
            'accounting/static/src/xml/warehouse_dashboard.xml',
        ],
    },
}