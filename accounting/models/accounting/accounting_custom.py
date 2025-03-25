from odoo import models, fields, api

class AccountMoveCustom(models.Model):
    _inherit = 'account.move'
    
    x_custom_reference = fields.Char('Custom Reference')
    
    @api.onchange('x_custom_reference')
    def _onchange_custom_reference(self):
        # Your custom logic here
        pass