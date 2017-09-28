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


class pit_school(models.Model):

    _name = "pit.school"
    _description = "school"

    code = fields.Char('Code' , index=True)
    name = fields.Char('Name')
    course_ids = fields.One2many('pit.school.course','school_id',string='Curses')
    teacher_id = fields.Many2one('pit.teacher','Teacher')

    active = fields.Boolean('Active', default=True)


class pit_school_course(models.Model):

    _name = "pit.school.course"
    _description = "Course"

    code = fields.Char('Code', index=True)
    name = fields.Char('Name')

    school_id = fields.Many2one('pit.school','school')
    teacher_id = fields.Many2one('pit.teacher','Teacher')

    product_ids = fields.One2many('pit.course.product','course_id',string='product')
    workload_ids = fields.One2many('pit.school.workload','course_id',string='Workloads')


    active = fields.Boolean('Active', default=True)

class pit_course_product(models.Model):

    _name = "pit.course.product"
    _description = "Course product"

    quant = fields.Float('Quant')
    product_id = fields.Many2one('product.product',string='Workloads')
    product_type = fields.Selection([('inscription','inscription'),('mensual','mensual'),('exam','exam')],string='type')
    course_id = fields.Many2one('pit.school.course','school')


class pit_school_workload(models.Model):

    _name = "pit.school.workload"
    _description = "Course workload"

    name = fields.Selection([('tehory','tehory'),('practical','practical'),('laboratory','laboratory')],string='type')
    workload = fields.Float('Workload' )
    course_id = fields.Many2one('pit.school.course','school')


class pit_school_course_group(models.Model):

    _name = "pit.school.course.group"
    _description = "Course group"

    code = fields.Char('Code', index=True)
    name = fields.Char('Name')
    course_id = fields.Many2one('pit.school.course','Course')

    date_from = fields.Date('from')
    date_to = fields.Date('to')
    teacher_id = fields.Many2one('pit.teacher','Teacher')
    company_id = fields.Many2one('res.company', 'Company', select=1)
    location_id = fields.Many2one('pit.location','Location')
    calendar_ids = fields.One2many('pit.school.course.calendar','group_id',string='Calendar')

    product_ids = fields.One2many('pit.group.product','group_id',string='product')

    active = fields.Boolean('Active', default=True)


    @api.depends('course_id')
    @api.onchange('course_id')
    def set_products(self):
        self.product_ids=False
        products =[]
        for product_id in self.course_id.product_ids :
            products.append((0,0,{'quant':product_id.quant,'product_id':product_id.product_id,'product_type':product_id.product_type}))
        self.name = self.course_id.name
        self.product_ids= products



class pit_group_product(models.Model):

    _name = "pit.group.product"
    _description = "group product"

    quant = fields.Float('Quant')
    product_id = fields.Many2one('product.product',string='Product')
    product_type = fields.Selection([('inscription','inscription'),('mensual','mensual'),('exam','exam'),('overdue','Overdue')],string='type')
    group_id = fields.Many2one('pit.school.course','school')


class pit_school_course_calendar(models.Model):

    _name = "pit.school.course.calendar"
    _description = "Course calendar"


    group_id = fields.Many2one('pit.school.course.group','Group')
    course_id = fields.Many2one('pit.school.course','Course',related='group_id.course_id')
    location_id = fields.Many2one('pit.location','Location',related='group_id.location_id')

    name = fields.Many2one('pit.school.workload','Workload' ,domain="[('course_id','=',course_id)]")
    dayofweek = fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of Week',default=0, required=True, select=True)
    date_from = fields.Date('Starting Date')
    date_to = fields.Date('End Date')
    hour_from = fields.Float('from', required=True, help="Start and End time of class.", select=True)
    hour_to = fields.Float("to", required=True)
    teacher_id = fields.Many2one('pit.teacher','Teacher')
    classroom_id = fields.Many2one('pit.location.classroom','Classroom',domain="[('location_id','=',location_id)]")







