# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class SaleBlanketOrder(models.Model):
    _name = 'sale.order.blanket'
    _description = 'Blanket Sale Order'

    #@api.model
    #def _get_domain_sequence_id(self):
    #    seq_type = self.env.ref('sale.seq_sale_order')
    #    return [('code', '=', seq_type.code)]


    name = fields.Char(string='Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    external_order = fields.Char(
        'External ID', size=10, required=True)    
    active = fields.Boolean(
        'Active', default=True)

    #sequence_id = fields.Many2one(
    #    comodel_name='ir.sequence', string='Entry Sequence', copy=False,
    #    domain=_get_domain_sequence_id)

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=False)
    sale_order_type_id = fields.Many2one('sale.order.type', 'Sale Order Type')
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Term')
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm')
    date_from = fields.Date(string="Valid From", default=fields.Date.today(), readonly=False)
    date_to = fields.Date(string="Valid To", default=fields.Date.today(), readonly=False)

