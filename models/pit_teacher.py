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


class pit_teacher(models.Model):

    _name = "pit.teacher"
    _description = "teacher"
    _inherits = {'res.partner': 'partner_id'}

   
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")

    code = fields.Char('Code' , index=True)
    emergency_contact = fields.Char('Emergency Contact')

   
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)

    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    allergies = fields.Char('Allergies' )

    employee_id = fields.Many2one('hr.employee', 'Employee')

    @api.multi
    def message_get_suggested_recipients(self):
        return self.partner_id.message_get_suggested_recipients()
    
    @api.multi
    def message_partner_info_from_emails(self, emails, link_mail=False):
        return self.partner_id.message_partner_info_from_emails( emails, link_mail)
    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, body='', subject=None, message_type='notification',
                     subtype=None, parent_id=False, attachments=None,
                     content_subtype='html', **kwargs):
        return self.partner_id.message_post(body, subject, message_type,
                     subtype, parent_id, attachments,
                     content_subtype, **kwargs)


    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['is_teacher'] = True
        return super(pit_teacher, self).create(vals)

    ## agrego compatibilidad con herencia de res_partner de estas funciones que no
    ## son heredadas 
    @api.multi
    def onchange_parent_id(self, parent_id):
        pass
    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {'value': {}}

    @api.one
    def create_employee(self):
        vals = {
            'name': self.name ,
            'address_home_id': self.partner_id.id
        }
        employee_id = self.env['hr.employee'].create(vals)
        self.write({'employee_id': employee_id.id})



    @api.one
    def send_user_link(self):
        user_id=self.env['res.users'].search([('partner_id','=',self.partner_id.id)],limit=1)
        if not self.email :
            raise ValidationError(_('Email is required.'))
        
        if len(user_id) == 0:
            user_id=self.env['res.users'].create({'name':self.name,'login':self.email,'partner_id':self.partner_id.id})
            group_id = self.env['ir.model.data'].get_object('pitman_base','pitman_teacher')
 
            group_id.write({'users': [(4, user_id.id)]})

        #user_id.action_reset_password()
 
