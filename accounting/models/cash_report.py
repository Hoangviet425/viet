# models/cash_report.py
from odoo import models, fields, api
from datetime import datetime, timedelta

class CashFlowReport(models.TransientModel):
    _name = 'cash.flow.report'
    _description = 'Báo cáo thu chi tiền mặt'
    
    date_from = fields.Date(string='Từ ngày', required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(string='Đến ngày', required=True, default=fields.Date.today())
    journal_ids = fields.Many2many('account.journal', string='Sổ quỹ', domain=[('type', '=', 'cash')])
    
    def _get_report_data(self):
        """Lấy dữ liệu báo cáo"""
        self.ensure_one()
        
        domain_receipts = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('state', '=', 'posted')
        ]
        
        domain_payments = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('state', '=', 'posted')
        ]
        
        if self.journal_ids:
            domain_receipts.append(('journal_id', 'in', self.journal_ids.ids))
            domain_payments.append(('journal_id', 'in', self.journal_ids.ids))
        
        receipts = self.env['cash.receipt'].search(domain_receipts)
        payments = self.env['cash.payment'].search(domain_payments)
        
        # Tính số dư đầu kỳ
        opening_balance = 0
        for journal in self.journal_ids or self.env['account.journal'].search([('type', '=', 'cash')]):
            accounts = journal.default_account_id
            if accounts:
                # Lấy số dư đầu kỳ từ các bút toán
                opening_moves = self.env['account.move.line'].search([
                    ('account_id', '=', accounts.id),
                    ('date', '<', self.date_from)
                ])
                for move in opening_moves:
                    opening_balance += move.debit - move.credit
        
        # Tính tổng thu và chi
        total_receipts = sum(receipts.mapped('amount'))
        total_payments = sum(payments.mapped('amount'))
        
        # Tính số dư cuối kỳ
        closing_balance = opening_balance + total_receipts - total_payments
        
        # Chi tiết các khoản thu chi
        receipt_details = []
        for receipt in receipts:
            receipt_details.append({
                'date': receipt.date,
                'name': receipt.name,
                'partner': receipt.partner_id.name or '',
                'reason': receipt.reason,
                'amount': receipt.amount,
                'journal': receipt.journal_id.name,
            })
        
        payment_details = []
        for payment in payments:
            payment_details.append({
                'date': payment.date,
                'name': payment.name,
                'partner': payment.partner_id.name or '',
                'reason': payment.reason,
                'amount': payment.amount,
                'journal': payment.journal_id.name,
            })
        
        return {
            'opening_balance': opening_balance,
            'total_receipts': total_receipts,
            'total_payments': total_payments,
            'closing_balance': closing_balance,
            'receipt_details': receipt_details,
            'payment_details': payment_details,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
    
    def action_print_report(self):
        """In báo cáo thu chi tiền mặt"""
        self.ensure_one()
        data = self._get_report_data()
        return self.env.ref('custom_cash_management.action_report_cash_flow').report_action(self, data=data)