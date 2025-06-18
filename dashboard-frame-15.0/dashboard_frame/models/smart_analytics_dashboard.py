from odoo import fields, models, _


class SmartAnalyticsDashboard(models.Model):
    _name = 'smart.analytics.dashboard'
    _description = 'Dashboard for Smart Analytics'
    _order = 'sequence, id'
    _inherit = ['image.mixin', 'mail.thread']
    _check_company_auto = True

    name = fields.Char('Name', required=True)
    url = fields.Char('Dashboard url', required=True)
    group_ids = fields.Many2many('res.groups', string="Access Groups")
    sequence = fields.Integer('Sequence', default=10)
    company_id = fields.Many2one('res.company', 'Company')
