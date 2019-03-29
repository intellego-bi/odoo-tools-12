# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_partner_ids(self):
        customers = self.env['res.partner'].search([('customer', '=', True)])   
        if self.blanket_partner_category_ids.id > 0:
            customers = self.env['res.partner'].search([('customer', '=', True), ('category_id', '=', self.blanket_partner_category_ids.id)])
        return customers

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
                                                    store=True,
                                                    comodel_name='res.partner.category',
                                                    relation='cl_blanket_partner_category_rel',
                                                    column1='sale_order_blanket_id',
                                                    column2='category_id')

    blanket_partner_ids = fields.Many2one('res.partner', 
                                  string='Partners from Blanket Order', 
                                  compute='_get_partner_ids', 
                                  readonly=True, 
                                  store=True)
                                                
    
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
                order.blanket_partner_ids = self._get_partner_ids()

    @api.multi
    @api.onchange('type_id', 'blanket_id', 'blanket_partner_category_ids')
    def onchange_blanket_partner_category_ids(self):
        for order in self:
            if order.blanket_partner_ids:
                order.blanket_partner_ids.invalidate_cache()
                order.blanket_partner_ids = self._get_partner_ids()
           


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
