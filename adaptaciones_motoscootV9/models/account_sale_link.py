# -*- coding: utf-8 -*-
from openerp import models, fields


class account_invoice(models.Model):
    _inherit = 'account.invoice'


        # This is the reverse link of the field 'invoice_ids' of sale.order
        # defined in addons/sale/sale.py
    sale_ids = fields.many2many(
            'sale.order', 'sale_order_invoice_rel', 'invoice_id',
            'order_id', 'Sale Orders', readonly=True,
            help="This is the list of sale orders related to this invoice.")
