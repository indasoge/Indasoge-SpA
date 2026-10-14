from odoo import _, fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    property_printing_action = fields.Selection(
        selection=[
            ('send_to_client', 'Send to Client'),
            ('open_print_dialog', 'Open Print Dialog'),
        ],
        string="Default Behavior",
        default='send_to_client',
    )

    def report_action(self, docids, data=None, config=True):
        action = super(IrActionsReport, self).report_action(
            docids, data=data, config=config
        )

        action['printing_action'] = self.property_printing_action

        return action

    def is_open_print_dialog(self):
        self.ensure_one()
        return self.property_printing_action == 'open_print_dialog'
