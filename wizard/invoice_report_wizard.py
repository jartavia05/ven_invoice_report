# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present Venture Technology. (<https://www.venturetech.site/>)


from datetime import date, datetime, timedelta
from odoo import models, fields, api
from . import xlsx_report_builder


class OutInvoiceReport(models.TransientModel):    
    _name = 'out_invoice.report'
    _description = 'Wizard to generate the xlsx report with customer sales'           

    date_start = fields.Date(string='Fecha de Inicio', required=True, default=datetime.now().strftime('%Y-%m-01'))
    date_end = fields.Date(string='Fecha de Fin', required=True, default=fields.Date.today)


    def print_xls_report(self):
        data = {
            'date_start': self.date_start, 
            'date_end': self.date_end,
            'type': 'out_invoice',
            'partner': 'Cliente'           
        }
              
        action = self.env.ref('ven_invoice_report.action_out_invoice_report_xls').report_action(self,data=data)
        action.update({'close_on_report_download': True}) 
        return action


class InInvoiceReport(models.TransientModel):
    _name = 'in_invoice.report'
    _description = 'Wizard to generate the xlsx report with vendor bills'           

    date_start = fields.Date(string='Fecha de Inicio', required=True, default=datetime.now().strftime('%Y-%m-01'))
    date_end = fields.Date(string='Fecha de Fin', required=True)


    def print_xls_report(self):
        data = {
            'date_start': self.date_start, 
            'date_end': self.date_end,
            'type': 'in_invoice',
            'partner': 'Proveedor'               
        }
              
        action = self.env.ref('ven_invoice_report.action_in_invoice_report_xls').report_action(self,data=data)
        action.update({'close_on_report_download': True}) 
        return action

  
class OutInvoiceXLSX(models.AbstractModel):
    _name = 'report.ven_invoice_report.out_invoice_report.xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, invoice):
        xlsx_report_builder.build_xlsx_report(self,workbook,data)


class InInvoiceXLSX(models.AbstractModel):
    _name = 'report.ven_invoice_report.in_invoice_report.xls'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, invoice):
        xlsx_report_builder.build_xlsx_report(self,workbook,data)


