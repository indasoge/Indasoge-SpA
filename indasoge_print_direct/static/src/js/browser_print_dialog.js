/** @odoo-module **/
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

/**
 * Generates the report url given a report action.
 *
 * @private
 * @param {ReportAction} action
 * @param {ReportType} type
 * @returns {string}
 */
function _getReportUrl(action, type, env) {
    let url = `/report/${type}/${action.report_name}`;
    const contextDict = Object.assign({} ,action.context, env.services.user.context);
    if (action.data && JSON.stringify(action.data) !== "{}") {
        // build a query string with `action.data` (it's the place where reports
        // using a wizard to customize the output traditionally put their options)
        const options = encodeURIComponent(JSON.stringify(action.data));
        const context = encodeURIComponent(JSON.stringify(contextDict));
        url += `?options=${options}&context=${context}`;
    } else {
        if (contextDict.active_ids) {
            url += `/${contextDict.active_ids.join(",")}`;
        }
        const context = encodeURIComponent(JSON.stringify(contextDict));
        url += `?context=${context}`;
    }
    return url;
}

/**
 * Launches download action of the report
 *
 * @private
 * @param {ReportAction} action
 * @param {ActionOptions} options
 * @returns {Promise}
 */
async function _openPrintDialog(action, options, env, type) {
    const url = _getReportUrl(action, type, env);
    printJS({
        printable: url,
        showModal: true,
        type: 'pdf',
        onPrintDialogClose: function () {
            const onClose = options.onClose;
            if (action.close_on_report_download) {
                return env.services.action.doAction({ type: "ir.actions.act_window_close" }, { onClose });
            } else if (onClose) {
                onClose();
            }
        },
    });
    return Promise.resolve(true)

}

let wkhtmltopdfStateProm;

registry.category("ir.actions.report handlers").add("open_print_dialog_handler", async (action, options, env) => {
    let is_open_browser_dialog = false
    if (action.printing_action && action.printing_action == 'open_print_dialog') {
        is_open_browser_dialog = true
    }
    else {
        is_open_browser_dialog = await env.services.rpc("/report/is_open_print_dialog", {report_ref: (action.id) ? action.id : action.report_name});
    }
    if (!is_open_browser_dialog)
        return Promise.resolve(false);

    if (action.report_type === "qweb-pdf") {
        // check the state of wkhtmltopdf before proceeding
        if (!wkhtmltopdfStateProm) {
            wkhtmltopdfStateProm = env.services.rpc("/report/check_wkhtmltopdf");
        }
        const state = await wkhtmltopdfStateProm;
        // display a notification according to wkhtmltopdf's state
        const link = '<br><br><a href="http://wkhtmltopdf.org/" target="_blank">wkhtmltopdf.org</a>';
        const WKHTMLTOPDF_MESSAGES = {
            broken:
                _t(
                    "Your installation of Wkhtmltopdf seems to be broken. The report will be shown " +
                        "in html."
                ) + link,
            install:
                _t(
                    "Unable to find Wkhtmltopdf on this system. The report will be shown in " + "html."
                ) + link,
            upgrade:
                _t(
                    "You should upgrade your version of Wkhtmltopdf to at least 0.12.0 in order to " +
                        "get a correct display of headers and footers as well as support for " +
                        "table-breaking between pages."
                ) + link,
            workers: _t(
                "You need to start Odoo with at least two workers to print a pdf version of " +
                    "the reports."
            ),
        };        
        if (state in WKHTMLTOPDF_MESSAGES) {
            env.services.notification.add(WKHTMLTOPDF_MESSAGES[state], {
                sticky: true,
                title: _t("Report"),
            });
        }
        if (state === "upgrade" || state === "ok") {
            // trigger the download of the PDF report
            return _openPrintDialog(action, options, env, "pdf");
        } else {
            // open the report in the client action if generating the PDF is not possible
            return Promise.resolve(false);
        }
    } else if (action.report_type === "qweb-text") {
        return _openPrintDialog(action, options, env, "text");
    }
});
