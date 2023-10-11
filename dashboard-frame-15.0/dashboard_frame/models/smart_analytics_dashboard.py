from odoo import api, fields, models, _


class SmartAnalyticsDashboard(models.Model):
    _name = 'smart.analytics.dashboard'
    _description = 'Dashboard for Smart Analytics'
    _order = 'sequence, id'
    _inherit = ['image.mixin']

    name = fields.Char(string='Name', required=True)
    url = fields.Char(string='Dashboard url', required=True)
    action_id = fields.Many2one('ir.actions.act_window', string='Action')
    menu_id = fields.Many2one('ir.ui.menu', string='Menu')
    group_ids = fields.Many2many('res.groups', string="Access Groups")
    sequence = fields.Integer(string='Sequence', default=10)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.menu_id:
                record.menu_id.write({
                    'groups_id': [(6, 0, record.group_ids.ids)] if record.group_ids else False,
                })
        return res

    def unlink(self):
        for record in self:
            record.remove_menu()
        return super().unlink()

    def create_menu(self):
        self.ensure_one()
        wizard = self.env['smart.analytics.dashboard.create.menu'].create({
            'dashboard_id': self.id,
            'name': self.name,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Menu'),
            'view_mode': 'form',
            'res_model': 'smart.analytics.dashboard.create.menu',
            'res_id': wizard.id,
            'target': 'new',
        }

    def remove_menu(self):
        self.ensure_one()
        if self.action_id:
            self.action_id.unlink()
        if self.menu_id:
            self.menu_id.unlink()
