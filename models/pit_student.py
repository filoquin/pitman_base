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
from openerp.exceptions import ValidationError

from openerp.tools.translate import _

import logging

_logger = logging.getLogger(__name__)


class pit_student(models.Model):

    _name = "pit.student"
    _description = "student"
    _inherits = {'res.partner': 'partner_id'}

    code = fields.Char('Code' , index=True)
    emergency_contact = fields.Char('Emergency Contact')
    family_ids = fields.One2many('pit.student.family','student_id','Family')
    #health_detail_ids = fields.One2many('pit_health_detail','student_id','Health')


    

   
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)
   
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")

    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    allergies = fields.Char('Allergies' )

    enrollment_ids = fields.One2many('pit.enrollment','student_id') 
    last_payment_fee = fields.Date('last fee',compute="_compute_last_fee",store=True) 
    current_debt = fields.Float('current debt',compute="_compute_current_debt",store=True) 
    active_course_ids = fields.One2many('pit.school.course','id',compute='_compute_active_course') 

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['is_student'] = True
        return super(pit_student, self).create(vals)


    @api.one
    def send_student_link(self):
        user_id=self.env['res.users'].search([('partner_id','=',self.partner_id.id)],limit=1)
        if not self.email :
            raise ValidationError(_('Email is required.'))
        
        if len(user_id) == 0:
            user_id=self.env['res.users'].create({'name':self.name,'login':self.email,'partner_id':self.partner_id.id})
            group_id = self.env['ir.model.data'].get_object('pitman_base','pitman_student')
 
            group_id.write({'users': [(4, user_id.id)]})

        #user_id.action_reset_password()
 

    @api.one
    @api.depends('enrollment_ids')
    def _compute_active_course(self):
        ids = []
        active_courses=self.env['pit.enrollment'].search([('state','=','active'),('student_id','=',self.id),('group_id.date_to','>',fields.Date.today())])
        for  enrollment in active_courses:
            ids.append(enrollment.group_id.course_id.id)
        self.active_course_ids = ids
 
    @api.one
    @api.depends('enrollment_ids')
    def _compute_current_debt(self):
        fees=self.env['pit.fee'].search([('student_id','=',self.id),('state','in',['unpaid','partial pay']),('date_due','<',fields.Date.today())])     
        amount= 0.0
        for x in fees:
            amount+=(x.amount - x.pay_amount) 
        self.current_debt=amount


    @api.one
    @api.depends('enrollment_ids')    
    def _compute_last_fee(self):
        last_fee=self.env['pit.fee'].search([('student_id','=',self.id),('state','=','pay')],
                                            limit=1,order="date_due DESC")
        if last_fee:
            self.last_payment_fee=last_fee.date_due

    @api.multi
    def recompute_student(self):
        self._compute_active_course()
        self._compute_current_debt()
        self._compute_last_fee()


    ## agrego compatibilidad con herencia de res_partner de estas funciones que no
    ## son heredadas 

    @api.multi
    def on_change_company_type(self, company_type):
        return {'value': {'is_company': company_type == 'company'}}


    @api.multi
    def onchange_parent_id(self, parent_id):
        pass
    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {'value': {}}

    @api.multi
    def list_fees(self):

   
        view = { 
            'name':"fee",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'tree',
            'res_model': 'pit.fee',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'self',
            'domain': '[("student_id","=",%d)]'%self.id,
        }
        return view



class pit_student_family(models.Model):

    _name = "pit.student.family"
    _description = "student family"

    student_id = fields.Many2one('pit.student','Student')
    relation = fields.Selection([('parent','parent'),('tutor','tutor')],'relation')
    partner_id = fields.Many2one('res.partner','Person')
    phone = fields.Char('Phone',related='partner_id.phone')

