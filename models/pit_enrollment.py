# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp import tools
from datetime import datetime , timedelta , date
from dateutil.relativedelta import relativedelta

from openerp.tools.translate import _

import logging

_logger = logging.getLogger(__name__)


DEFAULT_DUE_DAY = 10
DEFAULT_END_DAY = 10


class pit_enrollment(models.Model):

    _name = "pit.enrollment"
    _description = "enrollment"


    @api.model
    def default_date(self):
        return fields.Date.today()

    @api.model
    def _default_product_pricelist(self):
        return self.env['product.pricelist'].search([], limit=1)


    state = fields.Selection([('draft','Draft'),('active','active'),('cancel','cancel'),('abandoned','abandoned'),('finish','finish')],default='draft')

    student_id = fields.Many2one('pit.student', 'Student')
    current_debt = fields.Float('current debt',related='student_id.current_debt') 

    group_id = fields.Many2one('pit.school.course.group', 'group')
    date_from = fields.Date('from',related='group_id.date_from')
    date_to = fields.Date('to',related='group_id.date_to')
    course_id = fields.Many2one('pit.school.course','Course',related='group_id.course_id')

    enrollment_date = fields.Date('Date',default=lambda self: self.default_date())

    partner_id = fields.Many2one('res.partner', 'partner')    
    fees = fields.Integer('fees',default=1,min=1,max=12)
    pricelist_id = fields.Many2one('product.pricelist', 'pricelist',default=_default_product_pricelist)

    name = fields.Char('Name',compute="_compute_name")


    @api.model
    def _default_date(self):
        return fields.Date.context_today(self)


    @api.depends('student_id')
    @api.onchange('student_id')
    @api.one
    def _compute_partner(self):
        self.partner_id = self.student_id.partner_id.id


    @api.depends('student_id','group_id')
    @api.one
    def _compute_name(self):
        self.name = "%s %s" % (self.student_id.name , self.group_id.name)

    @api.one
    def save_data(self):
        ## todo validate datas
        self.state='draft'


    @api.one
    def do_cancel(self):
        
        fees = self.env["pit.fee"].search([('enrollment_id','=',self.id),('state','!=','pay')]).write({'state':'cancel'})        
        self.state='cancel'


    @api.one
    def do_enrollment(self):


        mensual_product_ids =[]
        mensual_amount = 0
        enrollment_product_ids =[]
        enrollment_amount = 0

        for product_line in self.group_id.product_ids:
            price = self.pricelist_id.price_get( product_line.product_id.id, 
                product_line.quant, self.partner_id.id)[self.pricelist_id.id]
            if product_line.product_type=='inscription':  
                enrollment_product_ids.append({'amount':price/self.fees,'quant':product_line.quant/self.fees,'product_id':product_line.product_id.id})
                enrollment_amount +=price/self.fees
            if product_line.product_type=='mensual':  
                mensual_product_ids.append({'amount':price/self.fees,'quant':product_line.quant/self.fees,'product_id':product_line.product_id.id})
                mensual_amount +=price


        product_ids =[]
        amount = 0

        for product_line in self.group_id.product_ids:
            if product_line.product_type=='inscription':
                price = self.pricelist_id.price_get( product_line.product_id.id, 
                    product_line.quant, self.partner_id.id)[self.pricelist_id.id]
  
                product_ids.append({'amount':price/self.fees,'quant':product_line.quant/self.fees,'product_id':product_line.product_id.id})
                amount +=price/self.fees


        enrollment_date=fields.Date.from_string(self.enrollment_date)

        if enrollment_date.day >= DEFAULT_END_DAY :
            date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) + relativedelta(months=1)
        else :
            date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) 


        if len(enrollment_product_ids):

            for fee_n in range(0, self.fees):


                fee={'name':'%i of %i'%(fee_n +1,self.fees),
                     'fee':fee_n +1,
                     'total_fee':self.fees,
                     #'product_ids':((6,0,product_ids)),
                     'amount':enrollment_amount,
                     'enrollment_id':self.id,
                     'partner_id':self.partner_id.id,                 
                     'product_type':'enrollment',
                     'date_due' : date_due,
                     }
                self.env['pit.fee'].create(fee)
                date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) + relativedelta(months=fee_n)

        self.state='active'

        from_date_due=fields.Date.from_string(self.group_id.date_from).replace(day=10) 

        to_date_due=fields.Date.from_string(self.group_id.date_to).replace(day=10) 

        i = 0
        currentDate = from_date_due
        while currentDate < to_date_due:
            _logger.info('currentDate %r'%currentDate)
            i += 1
            fee={'name':'mes %i'% i,
                 'fee':i,
                 'total_fee':mensual_amount,
                 #'product_ids':((6,0,product_ids)),
                 'amount':mensual_amount,
                 'enrollment_id':self.id,
                 'partner_id':self.partner_id.id,                 
                 'product_type':'mensual',
                 'date_due' : currentDate,
                 }
            self.env['pit.fee'].create(fee)
            currentDate += relativedelta(months=1)



        self.state='active'




class pit_fee(models.Model):

    _name = "pit.fee"
    _description = "fee"

    state = fields.Selection([('unpaid','unpaid'),('process','process pay'),('partial pay','partial pay'),('pay','pay'),('cancel','cancel')],default='unpaid')
    name = fields.Char('Name')
    fee = fields.Integer('fee N')
    total_fee = fields.Integer('Total Fee')

    enrollment_id = fields.Many2one('pit.enrollment', 'enrollment',ondelete='cascade')
    student_id = fields.Many2one('pit.student', 'Student',related="enrollment_id.student_id",store=True)
    partner_id = fields.Many2one('res.partner', 'partner')    
    product_type = fields.Selection([('enrollment','enrollment'),('mensual','mensual'),('exam','exam')],string='type')

    date_due = fields.Date('Date due')
    payment_day = fields.Date('Payment Date')
    amount = fields.Float('amount')
    pay_amount = fields.Float('amount')
    debt = fields.Float('debt',compute="_compute_debit",store=True)

    product_ids = fields.One2many('pit.fee.product','fee_id',string='product')

    @api.multi
    @api.depends('amount','pay_amount')
    def _compute_debit(self):
        for fee in self:
            fee.debt= fee.amount - fee.pay_amount

    @api.multi
    def do_cancel(self):
        self.state='cancel'
        


class pit_fee_product(models.Model):

    _name = "pit.fee.product"
    _description = "Fee product"

    quant = fields.Float('Quant')
    product_id = fields.Many2one('product.product',string='Product')
    fee_id = fields.Many2one('pit.fee','fee')
    amount = fields.Float('amount')

class pit_do_enrollment(models.TransientModel):


    _name = "pit.do_enrollment"
    _description = "Make enrollment"

    partner_id = fields.Many2one('res.partner', 'partner')    
    fees = fields.Integer('fees',default=1,min=1,max=12)
    pricelist_id = fields.Many2one('product.pricelist', 'pricelist')

    enrollment_id = fields.Many2one('pit.enrollment', 'enrollment')
    student_id = fields.Many2one('pit.student', 'Student',related="enrollment_id.student_id",store=True)
    group_id = fields.Many2one('pit.school.course.group', 'group',related="enrollment_id.group_id")


    date_from = fields.Date('Date from')


    @api.one
    def do(self):

        mensual_product_ids =[]
        mensual_amount = 0
        enrollment_product_ids =[]
        enrollment_amount = 0

        for product_line in self.enrollment_id.group_id.product_ids:
            price = self.pricelist_id.price_get( product_line.product_id.id, 
                product_line.quant, self.partner_id.id)[self.pricelist_id.id]
            if product_line.product_type=='inscription':  
                enrollment_product_ids.append({'amount':price/self.fees,'quant':product_line.quant/self.fees,'product_id':product_line.product_id.id})
                enrollment_amount +=price/self.fees
            if product_line.product_type=='mensual':  
                mensual_product_ids.append({'amount':price/self.fees,'quant':product_line.quant/self.fees,'product_id':product_line.product_id.id})
                mensual_amount +=price

        enrollment_date=fields.Date.from_string(self.enrollment_id.enrollment_date)

        if enrollment_date.day >= DEFAULT_DUE_DAY :
            date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) + relativedelta(months=1)
        else :
            date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) 


        for fee_n in range(0, self.fees):
            fee={'name':'%i of %i'%(fee_n +1,self.fees),
                 'fee':fee_n +1,
                 'total_fee':self.fees,
                 #'product_ids':((6,0,product_ids)),
                 'amount':enrollment_amount,
                 'enrollment_id':self.enrollment_id.id,
                 'partner_id':self.partner_id.id,                 
                 'product_type':'enrollment',
                 'date_due' : date_due,
                 }
            self.env['pit.fee'].create(fee)
            date_due = enrollment_date.replace(day=DEFAULT_DUE_DAY) + relativedelta(months=fee_n)




