# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
from odoo import models, fields, api, _
import xlwt
import base64
from io import StringIO
import datetime
from datetime import datetime

class CategoryReportOut(models.Model):        
    _name = 'category.report.out'
    _description = 'Product Category Quotation Report'
    
    file_name = fields.Char('Name', size=256)
    file_data = fields.Binary('Download Excel Report', readonly=True)


class Category_Quotation_Report(models.TransientModel):    
    _name = 'category.quotation.report'
    _description = 'Product Category Quotation Report'

    from_date = fields.Date('From',required=True)
    to_date = fields.Date('To',required=True)
    categ_ids = fields.Many2many('product.category', 'categ_report_vendor_quotation', 'report_id', 'categ_id', 'Product Categories')
    
    @api.multi
    def genarate_excel_report(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Category Wise Vendor Quotation", cell_overwrite_ok=True)
        #Style for Excel
        styleheading = xlwt.easyxf('font: name Arial, bold on;align: horiz center;')
        style0 = xlwt.easyxf('font: name Arial;align: horiz left;', num_format_str='0')        
        style1 = xlwt.easyxf('font: name Arial, bold on;align: horiz left;')
        money_format = xlwt.easyxf('font: name Arial, bold on;align: horiz right;', num_format_str='#,##0.00')
        sheet.col(0).width =5000
        sheet.col(1).width =15000        
        #Excel Heading Manipulation
        sheet.write_merge(0, 0, 0, 4, 'Category Wise Vendor Quotation Report', styleheading)                 
        sheet.write(2,0,'Sl.No', style1)
        sheet.write(2,1,'Category', style1)
       
        column = 2
        row = 3       
        pur_orders_vendor_goup = self.env['purchase.order'].read_group([('date_order','<=',self.to_date),
                                                                        ('date_order','>=',self.from_date),
                                                                        ],['id'],['partner_id'])
        
        pur_order_data = { res['partner_id'] : res['partner_id_count'] for res in pur_orders_vendor_goup }
        # Writing Vendor Columns
        for po in pur_order_data:
            sheet.col(column).width =6500
            sheet.write(2,column,str(po[1]), style1)            
            column = column + 1            
        for line in self.categ_ids:
            column = 2
            sheet.write(row,0, str(row-2), style1)
            sheet.write(row,1, str(line.name), style1)              
            for po in pur_order_data:
                quote_amount=0
                po_list=self.env['purchase.order'].search([('date_order','<=',self.to_date),
                                                            ('date_order','>=',self.from_date),
                                                            ('partner_id','=',po[0])])
                child_categ_ids=self.env['product.category'].search([('id', 'child_of', line.id)]).ids
                print("child_categ_ids....",child_categ_ids)                     
                for po_l in po_list:                      
                    po_l_lines = po_l.order_line.filtered(lambda r: r.product_id.categ_id.id in child_categ_ids ).mapped( "price_unit" )
                    quote_amount = quote_amount + sum(po_l_lines)
                sheet.write(row,column, str(quote_amount), style1)
                column = column + 1  
            row = row + 1                              
        workbook.save('/tmp/category_quote.xls')
        result_file = open('/tmp/category_quote.xls','rb').read()
        # Files actions         
        attach_vals = {
                'file_name': 'Category Wise Vendor Quotation Report'+ '.xls',
                'file_data': base64.encodestring(result_file),               
            } 
            
        act_id = self.env['category.report.out'].sudo().create(attach_vals)
        
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'category.report.out',
        'res_id': act_id.id,
        'view_type': 'form',
        'view_mode': 'form',
        'context': self.env.context,
        'target': 'new',
        }
   
                


