# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present Venture Technology. (<https://www.venturetech.site/>)
from odoo.exceptions import UserError

def build_xlsx_report(self, workbook, data):
    # Formating the Workbook
        row = 0
        row_lines = 0
        column = 0
        column_lines = 0
        sheet = workbook.add_worksheet('ventas' if data['type']=='out_invoice' else 'gastos')
        sheet_lines = workbook.add_worksheet('lineas_ventas' if data['type']=='out_invoice' else 'lineas_gastos')
        sheet.show_gridlines = False
        sheet_lines.show_gridlines = False
        bg_color = '#175487' if data['type']=='out_invoice' else '#59AF12'
        font_color = '#E8C440' if data['type']=='out_invoice' else '#040304'
        header_row_style = workbook.add_format({'bold':True, 'bg_color':bg_color, 'font_color':font_color})
        date_format = workbook.add_format({'num_format':'mm/dd/yyyy'})
        
        invoices_ids = self.env['account.invoice'].search([('type', '=', data['type']),
                                            ('state', 'in', ('open', 'paid')),
                                            ('date_invoice', '>=', data['date_start']),
                                            ('date_invoice', '<=', data['date_end']),
                                            ('company_id', 'in', tuple(self.env.user.company_ids.ids))
                                            ], order='id asc')
        if len(invoices_ids) >= 1:
            has_iva_devuelto = True if hasattr(invoices_ids[0], 'amount_total_iva_devuelto') else False
        else:
            raise UserError('No existen facturas en el periodo seleccionado')
            
            
        
        
        # Building the Invoice Sheet
        sheet.write(row,column, "Compañia", header_row_style)
        sheet.write(row,column+1, "Numero de Factura", header_row_style)
        sheet.write(row,column+2, "Estado FE", header_row_style)
        sheet.write(row,column+3, "Fecha", header_row_style)
        sheet.write(row,column+4, data['partner'], header_row_style)
        sheet.write(row,column+5, "Cedula", header_row_style)
        sheet.write(row,column+6, "Metodo de Pago", header_row_style)
        sheet.write(row,column+7, "Moneda", header_row_style)
        sheet.write(row,column+8, "Subtotal", header_row_style)
        sheet.write(row,column+9, "Impuesto", header_row_style)
        if has_iva_devuelto:
            sheet.write(row,column+10, "IVA Devuelto", header_row_style)
            sheet.write(row,column+11, "Total", header_row_style)
        else:
            sheet.write(row,column+10, "Total", header_row_style)

        # Building the Invoice_Line Sheet
        sheet_lines.write(row_lines,column_lines, "Compañia", header_row_style)
        sheet_lines.write(row_lines,column_lines+1, "Numero de Factura", header_row_style)
        sheet_lines.write(row_lines,column_lines+2, "Producto/Servicio", header_row_style)
        if data['type']=='out_invoice':
            sheet_lines.write(row_lines,column_lines+3, "Categoria", header_row_style)
            sheet_lines.write(row_lines,column_lines+4, "Cod. CABYS", header_row_style)
            sheet_lines.write(row_lines,column_lines+5, "Cantidad", header_row_style)
            sheet_lines.write(row_lines,column_lines+6, "Moneda", header_row_style)
            sheet_lines.write(row_lines,column_lines+7, "Precio Unitario", header_row_style)
            sheet_lines.write(row_lines,column_lines+8, "Subtotal", header_row_style)
            sheet_lines.write(row_lines,column_lines+9, "Impuesto", header_row_style)
            sheet_lines.write(row_lines,column_lines+10, "Total", header_row_style)
        else:
            sheet_lines.write(row_lines,column_lines+3, "Cantidad", header_row_style)
            sheet_lines.write(row_lines,column_lines+4, "Moneda", header_row_style)
            sheet_lines.write(row_lines,column_lines+5, "Precio Unitario", header_row_style)
            sheet_lines.write(row_lines,column_lines+6, "Subtotal", header_row_style)
            sheet_lines.write(row_lines,column_lines+7, "Impuesto", header_row_style)
            sheet_lines.write(row_lines,column_lines+8, "Total", header_row_style)

        
        
        for inv in invoices_ids:
            row += 1           
            if inv.currency_id.display_name == 'CRC':
                currency_format = workbook.add_format({'num_format':'[$₡-es-CR]#,##0.00'})
            elif inv.currency_id.display_name == 'USD':
                currency_format = workbook.add_format({'num_format':'[$$-409]#,##0.00'})
            else:
                currency_format = ''

            sheet.write(row,column,inv.company_id.name)
            sheet.write(row,column+1,inv.number)
            sheet.write(row,column+2,inv.state_tributacion)
            sheet.write(row,column+3,inv.date_due, date_format)
            sheet.write(row,column+4,inv.partner_id.display_name)
            sheet.write(row,column+5,inv.partner_id.vat)
            sheet.write(row,column+6,inv.payment_methods_id.display_name)
            sheet.write(row,column+7,inv.currency_id.display_name)
            sheet.write(row,column+8,inv.amount_untaxed, currency_format)
            sheet.write(row,column+9,inv.amount_tax, currency_format)
            if has_iva_devuelto:
                sheet.write(row,column+10,inv.amount_total_iva_devuelto, currency_format)
                sheet.write(row,column+11,inv.amount_total, currency_format)
            else: 
                sheet.write(row,column+10,inv.amount_total, currency_format)

            invoice_line_ids = self.env['account.invoice.line'].search([('invoice_id', '=', inv.id)])
            for lines in invoice_line_ids:
                row_lines +=1
                sheet_lines.write(row_lines,column_lines,lines.company_id.name)
                sheet_lines.write(row_lines,column_lines+1,lines.invoice_id.number)
                sheet_lines.write(row_lines,column_lines+2,lines.name)
                if data['type']=='out_invoice':
                    sheet_lines.write(row_lines,column_lines+3,lines.categ_name)
                    sheet_lines.write(row_lines,column_lines+4,lines.product_id.cabys_code)
                    sheet_lines.write(row_lines,column_lines+5,lines.quantity)
                    sheet_lines.write(row_lines,column_lines+6,lines.currency_id.display_name)
                    sheet_lines.write(row_lines,column_lines+7,lines.price_unit,currency_format)
                    sheet_lines.write(row_lines,column_lines+8,lines.price_subtotal,currency_format)
                    sheet_lines.write(row_lines,column_lines+9,lines.price_tax,currency_format)
                    sheet_lines.write(row_lines,column_lines+10,lines.price_total,currency_format)
                else:
                    sheet_lines.write(row_lines,column_lines+3,lines.quantity)
                    sheet_lines.write(row_lines,column_lines+4,lines.currency_id.display_name)
                    sheet_lines.write(row_lines,column_lines+5,lines.price_unit,currency_format)
                    sheet_lines.write(row_lines,column_lines+6,lines.price_subtotal,currency_format)
                    sheet_lines.write(row_lines,column_lines+7,lines.price_tax,currency_format)
                    sheet_lines.write(row_lines,column_lines+8,lines.price_total,currency_format)                    
        

        