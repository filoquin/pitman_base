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


class pit_career(models.Model):

    _name = "pit.career"
    _description = "career"

    code = fields.Char('Code' , index=True)
    name = fields.Char('Name' )
    course_ids = fields.One2many('pit.career.course','career_id','Career')
    teacher_id = fields.Many2one('pit.teacher','Teacher')
    workload_ids = fields.One2many('pit.career.workload','career_id','Workloads')

    active = fields.Boolean('Active' )



class pit_career_workload(models.Model):

    _name = "pit.career.workload"
    _description = "career workload"

    name = fields.Selection([('tehory','tehory'),('practical','practical'),('laboratory','laboratory')],string='type')
    workload = fields.Float('Workload' )
    career_id = fields.Many2one('pit.career','career')


class pit_career_course(models.Model):

    _name = "pit.career.course"
    _description = "Course"


    code = fields.Char('Code' , index=True)
    name = fields.Char('Name' )

    career_id = fields.Many2one('pit.career','career')
    teacher_id = fields.Many2one('pit.teacher','Teacher')
    company_id = fields.Many2one('res.company', 'Company', select=1),

    active = fields.Boolean('Active' )




class pit_career_course_calendar(models.Model):

    _name = "pit.career.course"
    _description = "Course calendar"


    name = fields.Many2one('pit.career.workload','career')
    dayofweek = fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of Week',default=0, required=True, select=True)
    date_from = fields.Date('Starting Date'),
    date_to = fields.Date('End Date'),
    hour_from = fields.Float('from', required=True, help="Start and End time of class.", select=True),
    hour_to = fields.Float("to", required=True),
    teacher_id = fields.Many2one('pit.teacher','Teacher')
    classroom_id = fields.Many2one('pit.Localion.classroom','Classroom')
    course_id = fields.Many2one('pit.career.course','Course')







