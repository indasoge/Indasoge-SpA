from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DashboardCreateMenu(models.TransientModel):
    _name = 'smart.analytics.dashboard.create.menu'
    _description = 'Create Menu for Smart analytics dashboard'

    dashboard_id = fields.Many2one('smart.analytics.dashboard', string='Dashboard', required=True, ondelete='cascade')
    parent_menu_id = fields.Many2one('ir.ui.menu', string='Parent Menu', ondelete='cascade')
    name = fields.Char(string='Menu Name')

    def menu_create(self):
        self.ensure_one()
        if not self.name:
            raise ValidationError(_('Menu name is required'))
        if not self.parent_menu_id:
            raise ValidationError(_('Parent menu is required'))

        view = self.env.ref('dashboard_frame.smart_analytics_dashboard_iframe_form')
        action = self.env['ir.actions.act_window'].create({
            'name': self.name,
            'res_model': 'smart.analytics.dashboard',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'res_id': self.dashboard_id.id,
        })
        self.dashboard_id.action_id = action
        menu = self.env['ir.ui.menu'].create({
            'name': self.name,
            'parent_id': self.parent_menu_id.id,
            'groups_id': [(6, 0, self.dashboard_id.group_ids.ids)] if self.dashboard_id.group_ids else False,
            'action': 'ir.actions.act_window,%d' % (action.id,)
        })
        self.dashboard_id.menu_id = menu
        return {'type': 'ir.actions.act_window_close'}
