
from odoo import api, models, fields, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    account_move_ids = fields.One2many(
        'account.move', 'payment_id', 'Journals Entry')
    state = fields.Selection(selection_add=[('cancelled', 'Cancelled')])

    def _create_payment_entry(self, amount):
        move = super(AccountPayment, self)._create_payment_entry(amount)
        move.payment_id = self.id
        return move

    @api.multi
    def reverse_payments(self):
        self.ensure_one()
        ctx = dict(self._context)
        ctx.update({
            'active_ids': self.account_move_ids.ids,
            'payment_id': self.id,
        })
        return {
            'name': _('Reverse Moves'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move.reversal',
            'view_id': self.env.ref(
                'account.view_account_move_reversal').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def re_generate(self, default=None):
        self.ensure_one()
        new_record = super(AccountPayment, self).copy(default=default)
        new_record.invoice_ids = self.invoice_ids
        return {
            'name': _('Draft Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'view_id': self.env.ref(
                'AccountPayment_transfer_account.view_AccountPayment_form_extend').id,
            'type': 'ir.actions.act_window',
            'res_id': new_record.id
        }
