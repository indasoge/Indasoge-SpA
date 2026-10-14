from odoo import http
from odoo.addons.web.controllers.report import ReportController, request


class DirectPrintReportController(ReportController):

    @http.route(['/report/is_open_print_dialog'], type='jsonrpc', auth="user")
    def is_open_print_dialog(self, report_ref):
        return request.env['ir.actions.report'].sudo()._get_report(report_ref).is_open_print_dialog()
