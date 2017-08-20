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


class pit_location(models.Model):

    _name = "pit.Localion"
    _description = "Location"

    code = fields.Char('Code', index=True)
    name = fields.Char('Name')
    classroom_ids = fields.One2many('pit.Localion.classroom','location_id','Workloads')
    company_id = fields.Many2one('res.company', 'Company', select=1),

    active = fields.Boolean('Active' )



class pit_location_classroom(models.Model):

    _name = "pit.Localion.classroom"
    _description = "Localion classroom"

    name = fields.Char('Name')
    location_id = fields.Many2one('pit.localion','Location')


