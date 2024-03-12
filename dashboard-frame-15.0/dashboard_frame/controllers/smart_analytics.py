# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SmartAnalytics(http.Controller):

    @http.route('/get/dashboard', type='json', website=False, auth='user')
    def get_dashboard(self):
        """
        This controller get all smart.analytics.dashboard filtered by company_ids
        and return data for owl app
        """
        company_ids = request.httprequest.cookies.get('cids', str(request.env.user.company_id.id))
        company_ids = [int(cid) for cid in company_ids.split(',')]
        data = request.env['smart.analytics.dashboard'].search(['|',
                                                                ('company_id', '=', False),
                                                                ('company_id', 'in', company_ids)])
        return data.read()

    @http.route('/get/url', type='json', website=False, auth='user')
    def get_url(self, item):
        """
        Browse smart.analytics.dashboard and return data to render.
        """
        dashboard = request.env['smart.analytics.dashboard'].browse(int(item))
        val = {'url': dashboard.url, 'name': dashboard.name}
        return val
