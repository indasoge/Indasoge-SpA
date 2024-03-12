# Copyright © 2021 Garazd Creation (<https://garazd.biz>)

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    ga4_debug_mode = fields.Boolean(string='Debug Mode')
    ga4_tracking_key = fields.Char(string='Tracking ID')

    def _ga4_params(self):
        self.ensure_one()
        return {'debug_mode': True} if self.ga4_debug_mode else {}

    def _ga4_configs(self):
        self.ensure_one()
        return [{
            'key': self.ga4_tracking_key or '',
            'params': self._ga4_params(),
        }]

    def ga4_get_primary_key(self):
        self.ensure_one()
        return self.ga4_tracking_key or ''
