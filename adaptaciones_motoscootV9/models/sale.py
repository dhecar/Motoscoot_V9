##############################################################################
#
# OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
from openerp import models, fields, api, exceptions


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    # STOCK IN EACH LOCATION
    @api.model
    def _compute_sum_stock(self):

        # db_obj = self.pool['base.external.dbsource']

        res = {}
        for line in self:
            if line.product_id:
                product = line.product_id.id
                location_id = 12
                # ads = db_obj.get_stock(cr, SUPERUSER_ID, ids, product, location_id,
                #                       context=context)

                self.env.cr.execute(""" SELECT SUM(qty) AS QTY, CASE
                            WHEN location_id='12' THEN 'G'
                            WHEN location_id='19' THEN 'B'
                            WHEN location_id='15' THEN 'P'
                            END AS LOC FROM stock_quant
                            WHERE (location_id ='12' OR location_id ='19' OR location_id='15')
                            AND product_id = '%s' GROUP BY location_id ORDER BY location_id""" % product)
                res[line.id] = self.env.cr.dictfetchall()

                if not res[line.id]:
                    res[line.id] = []
                else:
                    # GRN
                    if res[line.id][0]['loc'] == 'G':
                        # res[line.id][0]['qty'] = res[line.id][0]['qty'] - ads
                        res[line.id][0]['qty'] = res[line.id][0]['qty']
                counter = 0
                qty = ""
                qty_final = ""
                for location in res[line.id]:
                    counter += 1
                    qty += '  ' + str(res[line.id][counter - 1]['loc']) + "=" + str(
                        res[line.id][counter - 1]['qty']) + '    '
                qty_final += qty

                line.sum_stock = qty_final

    sum_stock = fields.Char(compute='_compute_sum_stock', string='Stocks')
    incoming = fields.Float(related='product_id.incoming_qty', string='IN')
    outgoing = fields.Float(related='product_id.outgoing_qty', string='OUT')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True)


SaleOrderLine()


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    sale_internal_comment = fields.Text(string='Internal Comment')
    picking_status = fields.Selection(related='picking_ids.state', string="Estado envio")
    # date_send = fields.Datetime(related='picking_ids.date_done', string="Fecha Envio")
    invoice_status = fields.Boolean(related='invoiced', string="Estado Factura")
    tracking = fields.Char(related='picking_ids.carrier_tracking_ref', string="Tracking")


SaleOrder()
