# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2017-TODAY Intellego Business Intelligence S.A.(<http://www.intellego-bi.com>).
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
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
###################################################################################


from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_order_type(self):
        return self.env['sale.order.type'].search([], limit=1)

        
    type_id = fields.Many2one(
        comodel_name='sale.order.type', string='Type', default=_get_order_type)

    blanket_id = fields.Many2one(
        comodel_name='sale.order.blanket',
        string='Blanket Sale Order')
    
    blanket_partner_category_ids = fields.Many2many(string='Partner Categories',
                                                    related='blanket_id.partner_category_ids',
                                                    readonly=True, 
                                                    store=False,
                                                    comodel_name='res.partner.category',
                                                    relation='cl_blanket_partner_category_rel',
                                                    column1='sale_order_id',
                                                    column2='category_id')
    
    so_type_require_blanket = fields.Boolean('Type Requires Blanket Order', related='type_id.require_blanket')


    @api.model
    def _get_blanket_per_order_type(self):
        sot_blanket_obj = self.env['sale.order.blanket']
        sot_blanket_id = sot_blanket_obj.search([('sale_order_type_id', '=', self.type_id.id)], limit=1)
        if sot_blanket_id:
            return sot_blanket_id
        else:
            if self.so_type_require_blanket:
                raise UserError('No se han encontrado Pedidos Marco para el tipo de pedido. '
                                'El tipo de pedido seleccionado requiere un Pedido Marco. '
                                'Imposible seleccionar este tipo de pedido. Ajuste su configuración.')
            return sot_blanket_obj
    
    
    @api.model
    def _compute_so_partner_ids(self):
        partner_obj = self.env['res.partner']
        if len(self.blanket_partner_category_ids) == 1:
            so_partner_obj_ids = partner_obj.search( [('customer', '=', True), ('category_id', '=', self.blanket_partner_category_ids.id)])
        elif len(self.blanket_partner_category_ids) > 1:
            so_partner_obj_ids = partner_obj.search( [('customer', '=', True), ('category_id', 'in', self.blanket_partner_category_ids)])
        else:
            so_partner_obj_ids = partner_obj.search( [('customer', '=', True)])
        so_partner_obj_ids = so_partner_obj_ids or []
        return [so_partner_obj_ids]
    
    so_partner_ids = fields.Many2many('res.partner', string='Partners by Categories',
                                      readonly=True,
                                      #store=False,
                                      relation='cl_sot_partner_category_rel',
                                      column1='sale_order_id',
                                      column2='partner_id')
                                  
    
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        sale_type = (self.partner_id.sale_type or
                     self.partner_id.commercial_partner_id.sale_type)
        if sale_type:
            self.type_id = sale_type
   
            
    @api.multi
    @api.onchange('type_id')
    def onchange_type_id(self):
        for order in self:
            if order.type_id.warehouse_id:
                order.warehouse_id = order.type_id.warehouse_id
            if order.type_id.picking_policy:
                order.picking_policy = order.type_id.picking_policy
            if order.type_id.payment_term_id:
                order.payment_term_id = order.type_id.payment_term_id.id
            if order.type_id.pricelist_id:
                order.pricelist_id = order.type_id.pricelist_id.id
            if order.type_id.incoterm_id:
                order.incoterm = order.type_id.incoterm_id.id
            if order.blanket_id:
                if order.blanket_id.sale_order_type_id != order.type_id:
                    order.blanket_id = []
                    order.blanket_partner_category_ids = []
            order.so_partner_ids = self._compute_so_partner_ids()
            order.blanket_id = order._get_blanket_per_order_type()
            
            
    @api.multi
    @api.onchange('blanket_id')
    def onchange_blanket_id(self):
        for order in self:
            if order.blanket_id.sale_order_type_id:
                order.type_id = order.blanket_id.sale_order_type_id
            if order.blanket_id.payment_term_id:
                order.payment_term_id = order.blanket_id.payment_term_id.id
            if order.blanket_id.pricelist_id:
                order.pricelist_id = order.blanket_id.pricelist_id.id
            if order.blanket_id.incoterm_id:
                order.incoterm = order.blanket_id.incoterm_id.id
            if order.blanket_id.partner_id:
                order.partner_id = order.blanket_id.partner_id.id
            if order.blanket_id.partner_category_ids:
                order.blanket_partner_category_ids = order.blanket_id.partner_category_ids
            order.so_partner_ids = self._compute_so_partner_ids()

    @api.multi
    @api.onchange('blanket_partner_category_ids')
    def onchange_blanket_partner_category_ids(self):
        so_partner_obj = self.env['res.partner']
        for so in self:
            if len(self.blanket_partner_category_ids) == 1:
                so.so_partner_ids = so_partner_obj.search([('customer', '=', True), ('category_id', '=', so.blanket_partner_category_ids.id)])
            elif len(self.blanket_partner_category_ids) > 1:
                so.so_partner_ids = so_partner_obj.search([('customer', '=', True), ('category_id', 'in', so.blanket_partner_category_ids)])
            else:
                so.so_partner_ids = so_partner_obj.search([('customer', '=', True)]) or []
         


    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/'and vals.get('type_id'):
            sale_type = self.env['sale.order.type'].browse(vals['type_id'])
            if sale_type.sequence_id:
                vals['name'] = sale_type.sequence_id.next_by_id()
        return super(SaleOrder, self).create(vals)

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.type_id.journal_id:
            res['journal_id'] = self.type_id.journal_id.id
        if self.type_id:
            res['sale_type_id'] = self.type_id.id
        if self.blanket_id:
            res['sale_blanket_id'] = self.blanket_id.id
        return res
