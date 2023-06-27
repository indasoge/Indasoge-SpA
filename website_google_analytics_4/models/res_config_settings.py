# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ga4_debug_mode = fields.Boolean(
        related='website_id.ga4_debug_mode',
        readonly=False,
    )

    @api.depends('website_id')
    def has_google_analytics_4(self):
        self.has_google_analytics_4 = bool(self.google_analytics_4_key)

    def inverse_has_google_analytics_4(self):
        if not self.has_google_analytics_4:
            self.google_analytics_4_key = False

    has_google_analytics_4 = fields.Boolean(
        string='Google Analytics 4',
        compute=has_google_analytics_4,
        inverse=inverse_has_google_analytics_4,
    )
