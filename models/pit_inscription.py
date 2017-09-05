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

from openerp.tools.translate import _

import logging

_logger = logging.getLogger(__name__)


class pit_inscription(models.Model):

    _name = "pit.inscription"
    _description = "inscription"

    name = fields.Char('Name')
    state = fields.Selection([('draft','Draft'),('active','active'),('cancel','cancel')],default='active')

    student_id = fields.Many2one('pit.student', 'Student')
    group_id = fields.Many2one('pit.school.course.group', 'group')
    inscription_date = fields.Date('Date')


class pit_fee(models.Model):

    _name = "pit.fee"
    _description = "fee"

    state = fields.Selection([('unpaid','unpaid'),('pay','pay'),('cancel','cancel')],default='unpaid')
    name = fields.Char('Name')
    fee = fields.Integer('fee N')
    total_fee = fields.Integer('Total Fee')

    inscription_id = fields.Many2one('pit.inscription', 'inscription')
    partner_id = fields.Many2one('res.partner', 'partner')    
    product_type = fields.Selection([('inscription','inscription'),('mensual','mensual'),('exam','exam')],string='type')

    date_due = fields.Date('Date due')
    payment_day = fields.Date('Payment Date')
    amount = fields.Float('amount')
    product_ids = fields.One2many('pit.fee.product','fee_id',string='product')

class pit_fee_poduct(models.Model):

    _name = "pit.fee.product"
    _description = "Fee product"

    quant = fields.Float('Quant')
    product_id = fields.Many2one('product.product',string='Product')
    fee_id = fields.Many2one('pit.fee','fee')
    amount = fields.Float('amount')

class pit_do_inscription(models.TransientModel):


    _name = "pit.do.inscription"
    _description = "Make inscription"

    partner_id = fields.Many2one('res.partner', 'partner')    
    fees = fields.Integer('fees',default=1,min=1,max=12)
    pricelist_id = fields.Many2one('product.pricelist', 'pricelist')

    inscription_id = fields.Many2one('pit.inscription', 'inscription')
    student_id = fields.Many2one('pit.student', 'Student',related="inscription_id.student_id",store=True)
    group_id = fields.Many2one('pit.school.course.group', 'group',related="inscription_id.student_id")


    date_from = fields.Date('Date from')


    @api.one
    def do(self):

        product_ids =[]
        amount = 0
        for product_line in inscription_id.group_id.product_ids:
            if product_line.product_type='inscription':

                price = self.env['product.pricelist'].price_get( [self.pricelist.id],
                            product_line.product_id.id, product_uom_qty, self.partner_id.id)[self.pricelist.id]

                product_ids.append({'quant':product_line.quant/self.fees,'product_id':product_line.product_id})



        for fee_n in range(1, self.fees):
            date_due =self.date_from
            product_ids = inscription_id.group_id.product_ids        



            fee={'name':'%f of %f'%(fee_n,self.fees),
                 'fee':fee_n,
                 'total_fee':self.fees,
                 'inscription_id':self.inscription_id,
                 'partner_id':None,                 
                 'product_type':'inscription',
                 'date_due' : date_due,
                 }

