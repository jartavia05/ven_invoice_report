# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present Venture Technology. (<https://www.venturetech.site/>)

{
    'name': "Reportes Factura Electronica Costa Rica",

    'summary': """
        Reporte de Facturacion Electronica Costa Rica""",

    'description': """
        Este modulo funciona para descargar un reporte en excel detallado de Ventas y Gastos de facturacion electronica, el cual incluye:

        - Compañia	
        - Numero de Factura	
        - Fecha	
        - Cliente o Proveedor	
        - Cedula	
        - Metodo de Pago	
        - Moneda	
        - Subtotal	
        - Impuesto	
        - Total  

    """,

    'author': "Venture Technology",
    'website': "https://www.venturetech.site",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': 
            [
            'base',
            'account',
            'report_xlsx',
            ],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'wizard/invoice_report_wizard.xml',
        'reports/invoice_report.xml',
    ],
}