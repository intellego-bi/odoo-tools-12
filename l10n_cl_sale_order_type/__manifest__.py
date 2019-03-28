# -*- coding: utf-8 -*-
###################################################################################
#
#    Intellego-BI.com
#    Copyright (C) 2019-TODAY Intellego Business Intelligence S.A.(<http://www.intellego-bi.com>).
#    Author: Rodolfo Bermúdez Neubauer(<https://www.intellego-bi.com>)
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
#    Copyright 2015 Carlos Sánchez Cifuentes <csanchez@grupovermon.com>
#    Copyright 2015-2016 Oihane Crucelaegui <oihane@avanzosc.com>
#    Copyright 2015-2018 Pedro M. Baeza <pedro.baeza@tecnativa.com>
#    Copyright 2016 Lorenzo Battistini
#    Copyright 2016 Carlos Dauden <carlos.dauden@tecnativa.com>
#    Copyright 2018 David Vidal <david.vidal@tecnativa.com>
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

{
    "name": "Chile - Sale Order Type",
    "version": "12.0.2.0.0",
    "category": "Sales Management",
    "author": "Intellego-BI.com,"
              "Grupo Vermon,"
              "AvanzOSC,"
              "Tecnativa,"
              "Agile Business Group,"
              "Niboo,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "license": "AGPL-3",
    "depends": [
        'sale_stock',
        'account',
        'sale_management',
    ],
    "demo": [
        "demo/sale_order_demo.xml",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/sale_order_view.xml",
        "views/sale_order_type_view.xml",
        "views/sale_order_blanket_view.xml",
        "views/account_invoice_view.xml",
        "views/res_partner_view.xml",
        "data/sale_price_list.xml",
        "data/sale_order_sequence.xml",
        "data/sale_order_type.xml",
    ],
    'installable': True,
}
