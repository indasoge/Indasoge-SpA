# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    ga4_debug_mode = fields.Boolean(string='Debug Mode')

    def _ga4_params(self, request=None):
        self.ensure_one()
        params = {}
        if self.ga4_debug_mode:
            params.update({'debug_mode': True})
        return params
