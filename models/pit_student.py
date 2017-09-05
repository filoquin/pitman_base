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


    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['is_student'] = True
        return super(pit_student, self).create(vals)

    @api.multi
    def on_change_company_type(self, company_type):
        return {'value': {'is_company': company_type == 'company'}}


    @api.multi
    def onchange_parent_id(self, parent_id):
        pass

class pit_student_family(models.Model):

    _name = "pit.student.family"
    _description = "student"

    student_id = fields.Many2one('pit.student','Student')
    relation = fields.Selection([('parent','parent'),('tutor','tutor')],'relation')
    partner_id = fields.Many2one('res.partner','Person')
    phone = fields.Char('Phone',related='partner_id.phone')
