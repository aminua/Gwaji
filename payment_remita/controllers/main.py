# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import http
from odoo.http import request

class RemitaController(http.Controller):
    
    @http.route('/payment/remita/return', type='http', auth='public', website=True)
    def remita_return(self, **post):
        tx = request.env['payment.transaction'].sudo().search([('id', '=', request.session.get('sale_transaction_id'))])
        if tx.state == 'pending' or tx.state == 'draft':
            tx.form_feedback(post, 'remita')
        return request.redirect('/payment/process')
