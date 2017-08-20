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
{
    'name': 'Pitman',
    'version': '9.0.1.0.0',
    'category': 'Education',
    "sequence": 1,
    'summary': 'Manage academy',
    'complexity': "easy",
    'description': """
        Small academy managing 
            * Student
            * teacher
            * Course
            * places
            * fees

    """,
    'author': 'Hormiga G',
    'website': 'http://www.hormigag.com.ar',
    'depends': ['base', 'product'],
    'data': [
        'views/pitman.xml',
        'views/pit_student.xml',
        'views/pit_teacher.xml',
    ],
    'demo': [
    ],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}


