# controllers/main.py
from odoo import http
from odoo.http import request

class CashDashboardController(http.Controller):
    @http.route('/cash_management/dashboard_data', type='json', auth='user')
    def get_dashboard_data(self):
        user = request.env.user
        company = user.company_id
        
        # Get cash journals
        journals = request.env['account.journal'].search([
            ('type', '=', 'cash'),
            ('company_id', '=', company.id)
        ])
        
        # Calculate totals
        total_receipts = request.env['cash.receipt'].search_count([
            ('state', '=', 'posted'),
            ('company_id', '=', company.id)
        ])
        
        total_payments = request.env['cash.payment'].search_count([
            ('state', '=', 'posted'),
            ('company_id', '=', company.id)
        ])
        
        # Get cash balance
        cash_balance = sum(journal.default_account_id.balance for journal in journals)
        
        return {
            'total_receipts': total_receipts,
            'total_payments': total_payments,
            'cash_balance': cash_balance,
            'currency_symbol': company.currency_id.symbol,
        }