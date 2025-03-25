from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CashReceipt(models.Model):
    _name = 'cash.receipt'
    _description = 'Phiếu thu tiền mặt'
    _order = 'date desc, id desc'
    
    name = fields.Char('Số phiếu', required=True, copy=False, default=lambda self: _('New'))
    date = fields.Date('Ngày', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string='Đối tác')
    amount = fields.Monetary('Số tiền', required=True)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', 
        default=lambda self: self.env.company.currency_id)
    reason = fields.Char('Lý do thu', required=True)
    journal_id = fields.Many2one('account.journal', string='Sổ nhật ký', 
        domain=[('type', '=', 'cash')], required=True)
    account_id = fields.Many2one('account.account', string='Tài khoản')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Xác nhận'),
        ('posted', 'Đã hạch toán'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft')
    move_id = fields.Many2one('account.move', string='Bút toán', readonly=True)
    company_id = fields.Many2one('res.company', string='Công ty', 
        default=lambda self: self.env.company)
    
    # Tương tự như MISA - tự động sinh số phiếu
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cash.receipt') or _('New')
        return super(CashReceipt, self).create(vals)
    
    # Hàm xác nhận phiếu thu
    def action_confirm(self):
        self.state = 'confirmed'
    
    # Hàm hạch toán vào sổ kế toán
    def action_post(self):
        for receipt in self:
            move_vals = {
                'journal_id': receipt.journal_id.id,
                'date': receipt.date,
                'ref': receipt.name,
                'line_ids': [
                    (0, 0, {
                        'name': receipt.reason,
                        'account_id': receipt.journal_id.default_account_id.id,
                        'debit': receipt.amount,
                        'credit': 0.0,
                        'partner_id': receipt.partner_id.id,
                    }),
                    (0, 0, {
                        'name': receipt.reason,
                        'account_id': receipt.account_id.id,
                        'debit': 0.0,
                        'credit': receipt.amount,
                        'partner_id': receipt.partner_id.id,
                    })
                ]
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            receipt.write({'state': 'posted', 'move_id': move.id})
    
    # Hàm hủy phiếu thu
    def action_cancel(self):
        for receipt in self:
            if receipt.move_id:
                receipt.move_id.button_cancel()
            receipt.state = 'cancelled'
    
    # Hàm đưa về nháp
    def action_draft(self):
        for receipt in self:
            receipt.state = 'draft'


class CashPayment(models.Model):
    _name = 'cash.payment'
    _description = 'Phiếu chi tiền mặt'
    _order = 'date desc, id desc'
    
    name = fields.Char('Số phiếu', required=True, copy=False, default=lambda self: _('New'))
    date = fields.Date('Ngày', required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one('res.partner', string='Đối tác')
    amount = fields.Monetary('Số tiền', required=True)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', 
        default=lambda self: self.env.company.currency_id)
    reason = fields.Char('Lý do chi', required=True)
    journal_id = fields.Many2one('account.journal', string='Sổ nhật ký', 
        domain=[('type', '=', 'cash')], required=True)
    account_id = fields.Many2one('account.account', string='Tài khoản')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Xác nhận'),
        ('posted', 'Đã hạch toán'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='draft')
    move_id = fields.Many2one('account.move', string='Bút toán', readonly=True)
    company_id = fields.Many2one('res.company', string='Công ty', 
        default=lambda self: self.env.company)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cash.payment') or _('New')
        return super(CashPayment, self).create(vals)
    
    # Hạch toán tương tự MISA
    def action_confirm(self):
        self.state = 'confirmed'
    
    def action_post(self):
        for payment in self:
            move_vals = {
                'journal_id': payment.journal_id.id,
                'date': payment.date,
                'ref': payment.name,
                'line_ids': [
                    (0, 0, {
                        'name': payment.reason,
                        'account_id': payment.account_id.id,
                        'debit': payment.amount,
                        'credit': 0.0,
                        'partner_id': payment.partner_id.id,
                    }),
                    (0, 0, {
                        'name': payment.reason,
                        'account_id': payment.journal_id.default_account_id.id,
                        'debit': 0.0,
                        'credit': payment.amount,
                        'partner_id': payment.partner_id.id,
                    })
                ]
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            payment.write({'state': 'posted', 'move_id': move.id})
    
    def action_cancel(self):
        for payment in self:
            if payment.move_id:
                payment.move_id.button_cancel()
            payment.state = 'cancelled'
    
    def action_draft(self):
        for payment in self:
            payment.state = 'draft'


class CashInventory(models.Model):
    _name = 'cash.inventory'
    _description = 'Kiểm kê quỹ tiền mặt'
    
    name = fields.Char('Mã kiểm kê', required=True, copy=False, default=lambda self: _('New'))
    date = fields.Date('Ngày kiểm kê', required=True, default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', string='Sổ quỹ', 
        domain=[('type', '=', 'cash')], required=True)
    theoretical_amount = fields.Monetary('Số dư sổ sách', readonly=True)
    counted_amount = fields.Monetary('Số dư thực tế')
    difference = fields.Monetary('Chênh lệch', compute='_compute_difference')
    currency_id = fields.Many2one('res.currency', related='journal_id.currency_id')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Xác nhận'),
    ], string='Trạng thái', default='draft')
    note = fields.Text('Ghi chú')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cash.inventory') or _('New')
        return super(CashInventory, self).create(vals)
    
    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id:
            self.theoretical_amount = self.journal_id.default_account_id.balance
    
    @api.depends('theoretical_amount', 'counted_amount')
    def _compute_difference(self):
        for rec in self:
            rec.difference = rec.counted_amount - rec.theoretical_amount
    # models/cash_management.py (thêm vào file đã có)

def get_monthly_data(self, year=None):
    """Lấy dữ liệu thu chi theo tháng cho biểu đồ"""
    self.ensure_one()
    if not year:
        year = fields.Date.today().year
        
    # Khởi tạo dữ liệu
    months = [str(i) for i in range(1, 13)]
    receipt_data = [0] * 12
    payment_data = [0] * 12
    
    # Lấy dữ liệu phiếu thu
    receipts = self.env['cash.receipt'].search([
        ('state', '=', 'posted'),
        ('date', '>=', f'{year}-01-01'),
        ('date', '<=', f'{year}-12-31')
    ])
    
    # Tính tổng theo tháng cho phiếu thu
    for receipt in receipts:
        month_index = receipt.date.month - 1
        receipt_data[month_index] += receipt.amount
    
    # Lấy dữ liệu phiếu chi
    payments = self.env['cash.payment'].search([
        ('state', '=', 'posted'),
        ('date', '>=', f'{year}-01-01'),
        ('date', '<=', f'{year}-12-31')
    ])
    
    # Tính tổng theo tháng cho phiếu chi
    for payment in payments:
        month_index = payment.date.month - 1
        payment_data[month_index] += payment.amount
    
    return {
        'labels': [f'Tháng {m}' for m in months],
        'receipts': receipt_data,
        'payments': payment_data
    }